# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class KatitaMassCreate(models.TransientModel):
    """Asistente para crear masivamente ítems que comparten la misma
    clasificación (línea, marca, modelo, género) pero varían por talla o por
    color. Cada ítem generado es un producto independiente (sin variantes)."""
    _name = 'katita.product.mass.create'
    _description = 'Creación masiva de ítems (Katita)'

    name = fields.Char(string='Nombre', required=True)
    standard_price = fields.Float(string='Costo (compra)')
    price_mode = fields.Selection(
        [('fixed', 'Precio directo'),
         ('percent', '% sobre costo'),
         ('extra', 'Costo + valor')],
        string='Modo de precio', default='fixed', required=True)
    list_price = fields.Float(string='Precio de venta')
    price_percent = fields.Float(string='% de ganancia')
    price_extra = fields.Float(string='Ganancia ($)')

    sale_ok = fields.Boolean(string='Ventas', default=True)
    purchase_ok = fields.Boolean(string='Compras', default=True)
    available_in_pos = fields.Boolean(string='Punto de venta', default=True,
                                      help='Los ítems creados estarán disponibles en el Punto de Venta.')
    is_storable = fields.Boolean(string='Rastrear inventario', default=True,
                                 help='Los ítems creados llevarán control de stock (cantidad a mano).')

    katita_linea_id = fields.Many2one('katita.linea', string='Línea', required=True)
    katita_marca_id = fields.Many2one('katita.marca', string='Marca', required=True)
    katita_modelo_id = fields.Many2one('katita.modelo', string='Modelo', required=True)
    katita_genero_id = fields.Many2one('katita.genero', string='Género', required=True)

    variation_type = fields.Selection(
        [('talla', 'Por talla'), ('color', 'Por color')],
        string='Variación', required=True, default='talla')

    # Variación por talla: lista de tallas + color fijo opcional.
    tallas = fields.Char(string='Tallas', help='Separadas por coma. Ej: 28,30,32')
    katita_color_id = fields.Many2one('katita.color', string='Color (fijo)',
                                      help='Color opcional aplicado a todas las tallas.')

    # Variación por color: varios colores + talla fija.
    color_ids = fields.Many2many('katita.color', string='Colores')
    talla = fields.Char(string='Talla (fija)')

    line_ids = fields.One2many('katita.product.mass.create.line', 'wizard_id',
                               string='Ítems a crear')

    def _line_price(self):
        """Precio de venta calculado según el modo elegido."""
        cost = self.standard_price or 0.0
        if self.price_mode == 'percent':
            return round(cost * (1 + (self.price_percent or 0.0) / 100.0), 2)
        if self.price_mode == 'extra':
            return round(cost + (self.price_extra or 0.0), 2)
        return self.list_price or 0.0

    def _build_line_vals(self):
        self.ensure_one()
        vals = []
        base = (self.name or '').strip()
        price = self._line_price()
        if self.variation_type == 'talla':
            tallas = [t.strip() for t in (self.tallas or '').replace(';', ',').split(',') if t.strip()]
            if not tallas:
                raise UserError(_('Ingrese al menos una talla.'))
            for talla in tallas:
                nombre = ' '.join(p for p in [base, talla] if p)
                vals.append((0, 0, {'name': nombre, 'color_id': self.katita_color_id.id,
                                    'talla': talla, 'list_price': price}))
        else:
            if not self.color_ids:
                raise UserError(_('Seleccione al menos un color.'))
            if not (self.talla or '').strip():
                raise UserError(_('Ingrese la talla.'))
            for color in self.color_ids:
                nombre = ' '.join(p for p in [base, color.name] if p)
                vals.append((0, 0, {'name': nombre, 'color_id': color.id,
                                    'talla': self.talla.strip(), 'list_price': price}))
        return vals

    def action_load(self):
        """Botón Cargar: arma la tabla de previsualización de los ítems."""
        self.ensure_one()
        self.line_ids = [(5, 0, 0)] + self._build_line_vals()
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }

    def action_create(self):
        """Botón Crear: genera un producto independiente por cada línea."""
        self.ensure_one()
        if not self.line_ids:
            raise UserError(_('Primero pulse "Cargar" para generar los ítems.'))
        products = self.env['product.template']
        pos_categoria = self.katita_linea_id.pos_category_id
        for line in self.line_ids:
            vals = {
                'name': line.name or self.name,
                'type': 'consu',
                'is_storable': self.is_storable,
                'list_price': line.list_price,
                'standard_price': self.standard_price,
                'sale_ok': self.sale_ok,
                'purchase_ok': self.purchase_ok,
                'available_in_pos': self.available_in_pos,
                'katita_linea_id': self.katita_linea_id.id,
                'katita_marca_id': self.katita_marca_id.id,
                'katita_modelo_id': self.katita_modelo_id.id,
                'katita_genero_id': self.katita_genero_id.id,
                'katita_color_id': line.color_id.id,
                'katita_talla': line.talla,
            }
            if pos_categoria:
                vals['pos_categ_ids'] = [(6, 0, pos_categoria.ids)]
            product = self.env['product.template'].create(vals)
            # El código se calcula solo; lo copiamos a la Referencia interna.
            product.default_code = product.katita_codigo
            products |= product
        return {
            'type': 'ir.actions.act_window',
            'name': _('Ítems creados'),
            'res_model': 'product.template',
            'view_mode': 'list,form',
            'domain': [('id', 'in', products.ids)],
        }


class KatitaMassCreateLine(models.TransientModel):
    _name = 'katita.product.mass.create.line'
    _description = 'Línea de creación masiva (Katita)'

    wizard_id = fields.Many2one('katita.product.mass.create', ondelete='cascade')
    name = fields.Char(string='Nombre')
    color_id = fields.Many2one('katita.color', string='Color')
    talla = fields.Char(string='Talla')
    list_price = fields.Float(string='Precio venta')
    codigo = fields.Char(string='Código', compute='_compute_codigo')

    @api.depends('wizard_id.katita_linea_id', 'wizard_id.katita_marca_id',
                 'wizard_id.katita_modelo_id', 'wizard_id.katita_genero_id',
                 'color_id', 'talla')
    def _compute_codigo(self):
        for line in self:
            wiz = line.wizard_id
            parts = [
                wiz.katita_linea_id.siglas,
                wiz.katita_marca_id.siglas,
                wiz.katita_modelo_id.siglas,
                line.color_id.siglas,
                wiz.katita_genero_id.numero,
                line.talla,
            ]
            line.codigo = ''.join(p for p in parts if p) or False
