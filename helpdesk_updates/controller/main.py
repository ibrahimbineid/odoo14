# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request
from odoo.addons.website_form.controllers.main import WebsiteForm


class WebsiteForm(WebsiteForm):

    @http.route('''/helpdesk/<model("helpdesk.team", "[('use_website_helpdesk_form','=',True)]"):team>/submit''', type='http', auth="public", website=True)
    def website_helpdesk_form(self, team, **kwargs):
        if not team.active or not team.website_published:
            return request.render("website_helpdesk.not_published_any_team")
        ticket_values = {}
        rejoin_obj = request.env['maintenance.region'].sudo().search([], order='id desc')
        city_obj = request.env['maintenance.city'].sudo().search([], order='id desc')
        location_obj = request.env['maintenance.location'].sudo().search([], order='id desc')
        ticket_values.update({
            'rejoin_obj': rejoin_obj,
            'city_obj': city_obj,
            'location_obj': location_obj,
        })

        default_values = {}
        if request.env.user.partner_id != request.env.ref('base.public_partner'):
            default_values['name'] = request.env.user.partner_id.name
            default_values['email'] = request.env.user.partner_id.email
        return request.render("website_helpdesk_form.ticket_submit",
                              {'team': team,
                               'default_values': default_values,
                               'ticket_values': ticket_values,
                               }
                              )

    # @http.route('/website_form/<string:model_name>', type='http', auth="public", methods=['POST'], website=True)
    # def website_form(self, model_name, **kwargs):
    #     if request.params.get('partner_email'):
    #         Partner = request.env['res.partner'].sudo().search([('email', '=', kwargs.get('partner_email'))], limit=1)
    #         if Partner:
    #             request.params['partner_id'] = Partner.id
    #     return super(WebsiteForm, self).website_form(model_name, **kwargs)