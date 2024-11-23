# -*- coding: utf-8 -*-
{
    'name': "Product Configurator Screen",
    'description': """
        Long description of module's purpose
    """,
    'author': "My Company",
    'website': "https://www.yourcompany.com",
    'version': '16.0.0.1',
    'license': 'LGPL-3',
    'depends': ['base', 'sale_management', 'stock'],
    'data': [
        'views/templates.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'product_configurator_screen/static/src/js/product_configurator.js',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}
