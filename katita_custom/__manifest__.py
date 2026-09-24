# -*- coding: utf-8 -*-
{
    'name': 'Katita - Customizaciones',
    'version': '19.0.1.1.0',
    'summary': 'Customizaciones a medida para el cliente Katita',
    'description': """
Módulo contenedor de las personalizaciones del cliente Katita.
Aquí se agregan modelos, vistas, reglas de acceso, datos y assets
específicos de este cliente, sin tocar los módulos base.
""",
    'author': 'Desarrollo personalizado',
    'category': 'Customizations',
    'license': 'LGPL-3',
    'depends': ['product', 'stock', 'point_of_sale'],
    'data': [
        'security/ir.model.access.csv',
        'data/katita_genero_data.xml',
        'views/katita_catalog_views.xml',
        'report/katita_qr_report.xml',
        'views/product_views.xml',
        'wizard/mass_create_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'katita_custom/static/src/js/select_create_dialog_patch.js',
            'katita_custom/static/src/xml/select_create_dialog.xml',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}
