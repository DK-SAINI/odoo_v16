from odoo import fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_dealer = fields.Boolean(string="Is Dealer")
    is_repairer = fields.Boolean(string="Is Repairer")