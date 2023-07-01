# -*- coding: utf-8 -*-
{
    "name": "Sale Systray Icon",
    "description": """
        Long description of module's purpose
    """,
    "author": "DK Company",
    "website": "https://www.dkcompany.com",
    "category": "Uncategorized",
    "version": "16.0.0.1",
    "depends": ["base", "sale_management"],
    "assets": {
        "web.assets_backend": {
            "/v16_systray_icon/static/src/js/icon_systray.js",
            "/v16_systray_icon/static/src/js/icon_dropdown.js",
            "/v16_systray_icon/static/src/xml/icon_systray.xml",
            "/v16_systray_icon/static/src/xml/icon_dropdown.xml",
        },
    },
}
