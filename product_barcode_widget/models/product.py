from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    custom_field_one = fields.Char()
