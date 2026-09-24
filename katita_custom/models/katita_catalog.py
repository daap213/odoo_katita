# -*- coding: utf-8 -*-
from odoo import api, fields, models


class KatitaLinea(models.Model):
    """Línea del producto (zapato, ropa, etc.). Las siglas forman el 1er
    segmento del código del ítem. Cada línea es un subconjunto de las
    categorías del Punto de Venta: al crearla se genera/enlaza su pos.category."""
    _name = 'katita.linea'
    _description = 'Línea (Katita)'
    _order = 'name'

    name = fields.Char(string='Nombre', required=True)
    siglas = fields.Char(string='Siglas', required=True,
                         help='Siglas usadas para armar el código del ítem.')
    observacion = fields.Text(string='Observación')
    pos_category_id = fields.Many2one(
        'pos.category', string='Categoría POS', readonly=True, ondelete='restrict',
        help='Categoría del Punto de Venta asociada a la línea (se crea automáticamente).')
    active = fields.Boolean(default=True)

    _siglas_unique = models.Constraint('UNIQUE(siglas)', 'Las siglas de línea deben ser únicas.')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('pos_category_id') and vals.get('name'):
                categoria = self.env['pos.category'].sudo().create({'name': vals['name']})
                vals['pos_category_id'] = categoria.id
        records = super().create(vals_list)
        records._katita_register_pos_category()
        return records

    def _katita_register_pos_category(self):
        """Agrega la categoría POS de la línea a los Puntos de Venta que
        restringen categorías, para que sus productos se muestren en el POS."""
        configs = self.env['pos.config'].sudo().search([('limit_categories', '=', True)])
        for rec in self:
            if not rec.pos_category_id:
                continue
            for config in configs:
                if rec.pos_category_id.id not in config.iface_available_categ_ids.ids:
                    config.sudo().iface_available_categ_ids = [(4, rec.pos_category_id.id)]

    def write(self, vals):
        res = super().write(vals)
        if vals.get('name'):
            for rec in self:
                if rec.pos_category_id and rec.pos_category_id.name != rec.name:
                    rec.pos_category_id.sudo().name = rec.name
        return res


class KatitaMarca(models.Model):
    """Marca del producto. Las siglas forman el 2do segmento del código."""
    _name = 'katita.marca'
    _description = 'Marca (Katita)'
    _order = 'name'

    name = fields.Char(string='Nombre', required=True)
    siglas = fields.Char(string='Siglas', required=True,
                         help='Siglas usadas para armar el código del ítem.')
    observacion = fields.Text(string='Observación')
    active = fields.Boolean(default=True)

    _siglas_unique = models.Constraint('UNIQUE(siglas)', 'Las siglas de marca deben ser únicas.')


class KatitaModelo(models.Model):
    """Modelo del producto. Las siglas forman el 3er segmento del código."""
    _name = 'katita.modelo'
    _description = 'Modelo (Katita)'
    _order = 'name'

    name = fields.Char(string='Nombre', required=True)
    siglas = fields.Char(string='Siglas', required=True,
                         help='Siglas usadas para armar el código del ítem.')
    observacion = fields.Text(string='Observación')
    active = fields.Boolean(default=True)

    _siglas_unique = models.Constraint('UNIQUE(siglas)', 'Las siglas de modelo deben ser únicas.')


class KatitaColor(models.Model):
    """Color del producto. Es opcional en el ítem; si se especifica, su sigla
    se agrega al código."""
    _name = 'katita.color'
    _description = 'Color (Katita)'
    _order = 'name'

    name = fields.Char(string='Nombre', required=True)
    siglas = fields.Char(string='Siglas', required=True,
                         help='Siglas usadas para armar el código del ítem cuando se especifica el color.')
    observacion = fields.Text(string='Observación')
    active = fields.Boolean(default=True)

    _siglas_unique = models.Constraint('UNIQUE(siglas)', 'Las siglas de color deben ser únicas.')


class KatitaGenero(models.Model):
    """Género del producto. El número forma un segmento del código:
    Masculino=01, Femenino=02, Niño=03, Niña=04, Unisex=05."""
    _name = 'katita.genero'
    _description = 'Género (Katita)'
    _order = 'numero'

    name = fields.Char(string='Nombre', required=True)
    numero = fields.Char(string='Número', required=True,
                         help='Número usado para armar el código del ítem (01, 02, ...).')
    active = fields.Boolean(default=True)

    _numero_unique = models.Constraint('UNIQUE(numero)', 'El número de género debe ser único.')
