# -*- coding: utf-8 -*-

import logging

from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.session import Session
from odoo.addons.web.controllers.home import Home

_logger = logging.getLogger(__name__)


class SessionWebsite(Session):

    @http.route('/web/session/logout', type='http', auth="none")
    def logout(self, redirect='/web'):

        # When user logut set hide_menu field value False.
        website_menu = http.request.env['website.menu'].sudo().search([('website_id', '=', http.request.website.id)])        
        for menu in website_menu:
            menu.sudo().update({'hide_menu': False})

        result = super().logout(redirect=redirect)
        return result

class Home(Home):

    @http.route('/web/login', type='http', auth="none")
    def web_login(self, redirect=None, **kw):
        response = super().web_login(redirect=redirect, **kw)

        # Check if the user is logged in
        if http.request.session.uid:
            # Get the logged-in user
            user = http.request.env.user
            # Check if the user has a linked partner (customer)
            if user.partner_id:
                # Check if the linked partner is a dealer
                if user.partner_id.is_dealer:
                    # Set the hide_menu field of the current website's menu to True
                    website_menu = http.request.env['website.menu'].sudo().search([('website_id', '=', http.request.website.id)])
                    for menu in website_menu:
                        if menu.name in ['Shop', 'News']:
                            menu.sudo().update({'hide_menu': True})
                else:
                    _logger.info("User is not a dealer")
            else:
                _logger.info("User does not have a linked partner (customer)")
        else:
            _logger.info("User is not logged in")

        return response