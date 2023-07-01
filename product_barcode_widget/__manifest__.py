# -*- coding: utf-8 -*-
{
    "name": "Product Barcode Widget",
    "description": "Long description of module's purpose",
    "author": "My Company",
    "website": "https://www.dk.com",
    "version": "16.0.0.1",
    "depends": ["base", "sale_management"],
    "data": [
        "views/product.xml",
    ],
    "assets": {
        "web.assets_backend": {
            "/product_barcode_widget/static/src/lib/JsBarcode.all.min.js",
            "/product_barcode_widget/static/src/barcode/barcode.js",
            "/product_barcode_widget/static/src/barcode/barcode.xml",
        },
    },
}
