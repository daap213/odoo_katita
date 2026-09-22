# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # Clasificación Katita (se muestran como selectores en el ítem).
    katita_linea_id = fields.Many2one('katita.linea', string='Línea')
    katita_marca_id = fields.Many2one('katita.marca', string='Marca')
    katita_modelo_id = fields.Many2one('katita.modelo', string='Modelo')
    katita_color_id = fields.Many2one('katita.color', string='Color')
    katita_genero_id = fields.Many2one('katita.genero', string='Género')
    katita_talla = fields.Char(string='Talla')

    # Cómo se determina el precio de venta a partir del costo.
    katita_price_mode = fields.Selection(
        [('fixed', 'Precio directo'),
         ('percent', '% sobre costo'),
         ('extra', 'Costo + valor')],
        string='Modo de precio', default='fixed', required=True)
    katita_price_percent = fields.Float(string='% de ganancia')
    katita_price_extra = fields.Float(string='Ganancia ($)')

    @api.onchange('katita_price_mode', 'katita_price_percent',
                  'katita_price_extra', 'standard_price')
    def _onchange_katita_price(self):
        for prod in self:
            cost = prod.standard_price or 0.0
            if prod.katita_price_mode == 'percent':
                prod.list_price = round(cost * (1 + (prod.katita_price_percent or 0.0) / 100.0), 2)
            elif prod.katita_price_mode == 'extra':
                prod.list_price = round(cost + (prod.katita_price_extra or 0.0), 2)
            # 'fixed': el usuario escribe el precio directamente.

    # Código del ítem que se imprime como QR. Se arma automáticamente con:
    # Línea.siglas + Marca.siglas + Modelo.siglas + [Color.sigla] + Género.número + Talla
    # (color solo participa si se especifica). Por ahora sin separador.
    katita_codigo = fields.Char(string='Código (QR)', compute='_compute_katita_codigo',
                                store=True, readonly=True)

    @api.depends('katita_linea_id.siglas', 'katita_marca_id.siglas',
                 'katita_modelo_id.siglas', 'katita_color_id.siglas',
                 'katita_genero_id.numero', 'katita_talla')
    def _compute_katita_codigo(self):
        for prod in self:
            parts = [
                prod.katita_linea_id.siglas,
                prod.katita_marca_id.siglas,
                prod.katita_modelo_id.siglas,
                prod.katita_color_id.siglas,   # opcional: vacío si no hay color
                prod.katita_genero_id.numero,
                prod.katita_talla,
            ]
            prod.katita_codigo = ''.join(p for p in parts if p) or False

    @api.onchange('katita_linea_id')
    def _onchange_katita_linea(self):
        """La línea es un subconjunto de las categorías del POS: al elegirla, se
        asigna su categoría del Punto de Venta."""
        if self.katita_linea_id.pos_category_id:
            self.pos_categ_ids = [(6, 0, self.katita_linea_id.pos_category_id.ids)]

    def action_print_katita_qr(self):
        """Imprime el código del ítem como QR usando el generador nativo de
        Odoo (ir.actions.report.barcode)."""
        self.ensure_one()
        return self.env.ref('katita_custom.action_report_katita_qr').report_action(self)
