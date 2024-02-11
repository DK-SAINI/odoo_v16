# -*- coding: utf-8 -*-
{
    'name': "hide_website_menu",
    'summary': """
            Hide website menu
        """,
    'description': """
        Hide Website Menu Using Boolean Field hide_menu in website.menu object base on user --> partner_id.
    """,
    'author': "My Company",
    'website': "https://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'web', 'website'],

    # always loaded
    'data': [
        'views/res_partner_views.xml',
        'views/website_templates.xml',
    ],
    'install': True
}
