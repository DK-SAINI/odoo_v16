# -*- coding: utf-8 -*-
{
    "name": "AMT Catalogue Synch",
    "version": "16.0.0.1",
    "author": "Strategic Dimensions'",
    "category": "",
    "website": "www.strategicdimensions.co.za",
    "summary": "AMT Catalogue Synchronisation Module",
    "depends": ["base", "product"],
    "data": [
        "security/ir.model.access.csv",
        "views/catalogue_configuration.xml",
        "views/product_view.xml",
        "views/menu.xml",
    ],
    # "assets": {
    #     "web.assets_backend": [
    #         "amt_catalogue_synch/static/src/webclient/home_menu/connection_panel.js",
    #         "amt_catalogue_synch/static/src/webclient/home_menu/connection_panel.xml",
    #         "amt_catalogue_synch/static/src/webclient/home_menu/home_menu.xml",
    #     ]
    # },
    "installable": True,
    "auto_install": False,
    "license": "LGPL-3",
}
