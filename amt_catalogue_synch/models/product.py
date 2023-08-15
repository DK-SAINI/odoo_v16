from odoo import models, fields


class ProductTemplateInherit(models.Model):
    _inherit = "product.template"

    compatibility = fields.Text(string="Compatibility", readonly=True)
