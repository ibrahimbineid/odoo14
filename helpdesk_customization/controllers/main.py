# -*- coding: utf-8 -*-


from odoo import http
from odoo import models, api
from odoo.http import request, Controller, route
from odoo.addons.portal.controllers.portal import pager as portal_pager, CustomerPortal
from odoo.tools.translate import _
from odoo.addons.website_form.controllers.main import WebsiteForm


class ShowDelivery(WebsiteForm):

    @http.route(['/get/select_region/'], type='json', auth="public", website=True)
    def selct_region_name(self, city_id, **kw):
        if city_id:
            city_ids = request.env['maintenance.city'].sudo().browse(int(city_id))
            if city_ids:
                return city_ids[0].region_id.id

    @http.route(['/get/select_region_city/'], type='json', auth="public", website=True)
    def select_region_city_name(self, location_id, **kw):
        if location_id:
            location_ids = request.env['maintenance.location'].sudo().browse(int(location_id))
            if location_ids:
                return [location_ids[0].region_id.id,location_ids[0].city_id.id]

    @http.route(['/get/select_region_city_location/'], type='json', auth="public", website=True)
    def select_region_city_location_name(self, sites_id, **kw):
        if sites_id:
            sites_ids = request.env['maintenance.equipment'].sudo().browse(int(sites_id))
            if sites_ids:
                return [sites_ids[0].region_id.id, sites_ids[0].city_id.id,sites_ids[0].location_id.id]

    @http.route(['/get/city_list'], type='json', auth="public", website=True)
    def get_city_name(self,region_id, **kw):
        if region_id:
            city_ids = request.env['maintenance.city'].sudo().search([('region_id','=',int(region_id))])

        if not city_ids:
            city_ids = request.env['maintenance.city'].sudo().search([])

        return dict(
            city_list=[(st.id, st.name) for st in city_ids],
        )

    @http.route(['/get/location_list'], type='json', auth="public", website=True)
    def get_location_name(self, region_id,city_id, **kw):
        if region_id:
            location_ids = request.env['maintenance.location'].sudo().search([('region_id','=',int(region_id)),('city_id','=',int(city_id))])
        else:
            location_ids = request.env['maintenance.location'].sudo().search([('city_id', '=', int(city_id))])

        if not location_ids:
            location_ids = request.env['maintenance.location'].sudo().search([])

        return dict(
            location_list=[(st.id, st.name) for st in location_ids],
        )

    @http.route(['/get/sites_list'], type='json', auth="public", website=True)
    def get_sites_name(self, region_id, city_id,location_id, **kw):
        if region_id and city_id and location_id:
            sites_ids = request.env['maintenance.equipment'].sudo().search([
                ('region_id','=',int(region_id)),
                ('city_id','=',int(city_id)),
                ('location_id','=',int(location_id))
            ])

        elif city_id and location_id:
            sites_ids = request.env['maintenance.equipment'].sudo().search([
                ('city_id','=',int(city_id)),
                ('location_id','=',int(location_id))
            ])
        elif location_id:
            sites_ids = request.env['maintenance.equipment'].sudo().search([
                ('location_id','=',int(location_id))
            ])
        if not sites_ids:
            sites_ids = request.env['maintenance.equipment'].sudo().search([])

        return dict(
            sites_list=[(st.id, st.name) for st in sites_ids],
        )


    @http.route(['/helpdesk/'], type='http', auth="public", website=True)
    def delivery_order_total(self, **kwargs):
        ticket_values = {}
        rejoin_obj = request.env['maintenance.region'].sudo().search([], order='id desc')
        city_obj = request.env['maintenance.city'].sudo().search([], order='id desc')
        location_obj = request.env['maintenance.location'].sudo().search([], order='id desc')
        ticket_values.update({
            'rejoin_obj': rejoin_obj,
            'city_obj': city_obj,
            'location_obj': location_obj,
        })
        site = request.env['maintenance.equipment'].sudo().search([])

        default_values = {}
        if request.env.user.partner_id != request.env.ref('base.public_partner'):
            default_values['name'] = request.env.user.partner_id.name
            default_values['email'] = request.env.user.partner_id.email

        return http.request.render('helpdesk_customization.ticket_submit_form_new', {
            'default_values': default_values,
            'ticket_values': ticket_values,
            'sites': site,
            'regions': rejoin_obj,
            'locations': location_obj,
            'cities': city_obj,
        })

    @http.route(['/helpdesk/created'], type='http', auth="public", website=True)
    def create_ticket(self, **kwargs):
        print('Heloooo')

    @http.route(['/helpdesk/created'], type='http', auth="public", website=True)
    def create_ticket(self, **kwargs):
        print('Hello')
        partner_id = request.env['res.partner'].sudo().search([('name', '=', kwargs.get('partner_name'))], limit=1)
        if not partner_id:
            partner_vals = {
                'name': kwargs.get('partner_name'),
                'email': kwargs.get('partner_email'),
            }
            partner_id = request.env['res.partner'].sudo().create(partner_vals)
        print(int(kwargs.get('region')))
        site_id = request.env['maintenance.equipment'].sudo().browse([int(kwargs.get('site'))])
        region_id = request.env['maintenance.region'].sudo().search([('id', '=', int(kwargs.get('region')))],
                                                                    limit=1)
        # region_id = request.env['maintenance.region'].browse([int(kwargs.get('region'))])
        location = request.env['stock.location'].sudo().search([('name', '=', site_id.location_id.name)],
                                                               limit=1)
        print(location)
        location_src = request.env['stock.location'].sudo().search(
            [('name', '=', region_id.name), ('location_id.name', '=', 'WH')], limit=1)

        ticket_val = {
            'name': kwargs.get('name'),
            'partner_id': partner_id.id,
            'description': kwargs.get('description'),
            'maintenance_equipment_id': kwargs.get('site'),
            'location_id': kwargs.get('location'),
            'region_id': kwargs.get('region'),
            'city_id': kwargs.get('city'),
            # 'maintenance_equipment_category_id': site_type,
            'location_src_id': location_src.id,
            'location_dest_id': location.id,
        }
        if site_id.category_id:
            ticket_val['maintenance_equipment_category_id'] = site_id.category_id.id

        t = request.env['helpdesk.ticket'].sudo().create(ticket_val)
        return request.render("helpdesk_customization.ticket_success", {})