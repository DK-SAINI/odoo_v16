# -*- coding: utf-8 -*-

from odoo import models, fields, api


class website(models.Model):
    _inherit = 'website.menu'

    hide_menu = fields.Boolean()
    

