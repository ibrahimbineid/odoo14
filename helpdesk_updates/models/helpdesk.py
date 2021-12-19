# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)
grey = "\x1b[38;21m"
yellow = "\x1b[33;21m"
red = "\x1b[31;21m"
bold_red = "\x1b[31;1m"
reset = "\x1b[0m"
green = "\x1b[32m"
blue = "\x1b[34m"


class MaintenanceEquipment(models.AbstractModel):
    _inherit = "maintenance.equipment"

    @api.onchange('location_id')
    @api.depends('location_id.site_type_ids')
    def _get_categories_domain(self):
        category_list = []
        if self.location_id:
            if self.location_id.site_type_ids:
                category_list = self.location_id.site_type_ids.ids
        else:
            category_list = self.env['maintenance.equipment.category'].search([]).ids
        return {'domain': {'category_id': [('id', 'in', category_list)]}}

    region_id = fields.Many2one('maintenance.region', required=1)
    city_id = fields.Many2one('maintenance.city', required=1)
    location_id = fields.Many2one('maintenance.location', required=1)
    category_id = fields.Many2one('maintenance.equipment.category', string='Site Type', domain=_get_categories_domain)

    @api.onchange('region_id')
    def change_region_id(self):
        for record in self:
            if record.region_id:
                city_ids = self.env['maintenance.city']. \
                    search([('region_id.id', '=', record.region_id.id)])
                cities = []
                for city in city_ids:
                    cities.append(city.id)
                domain = {'city_id': [('id', 'in', cities)]}
                return {'domain': domain}

    @api.onchange('city_id')
    def change_city_id(self):
        for record in self:
            if record.city_id:
                location_ids = self.env['maintenance.location']. \
                    search([('city_id.id', '=', record.city_id.id)])
                locations = []
                for location in location_ids:
                    locations.append(location.id)
                domain = {'location_id': [('id', 'in', locations)]}
                return {'domain': domain}

    @api.onchange('location_id')
    def change_location_id(self):
        for record in self:
            if record.location_id:
                if not record.city_id:
                    record.city_id = record.location_id.city_id
                if not record.region_id:
                    record.region_id = record.location_id.region_id


class MaintenanceRequest(models.AbstractModel):
    _inherit = "maintenance.request"

    @api.onchange('location_id')
    @api.depends('location_id.site_type_ids')
    def _get_categories_domain(self):
        category_list = []
        if self.location_id:
            if self.location_id.site_type_ids:
                category_list = self.location_id.site_type_ids.ids
        else:
            category_list = self.env['maintenance.equipment.category'].search([]).ids
        return {'domain': {'category_id': [('id', 'in', category_list)]}}

    equipment_id = fields.Many2one('maintenance.equipment', string='Site Name',
                                   ondelete='restrict', index=True, check_company=True)
    category_id = fields.Many2one('maintenance.equipment.category', string='Site Type',
                                  store=True, readonly=False, domain=_get_categories_domain)

    maintenance_type = fields.Selection([('corrective', 'Corrective'),
                                         ('preventive', 'Preventive')
                                         ],
                                        string='Maintenance Type', default="preventive")
    region_id = fields.Many2one('maintenance.region', required=1)
    city_id = fields.Many2one('maintenance.city', required=1)
    location_id = fields.Many2one('maintenance.location', required=1)

    @api.onchange('region_id')
    def change_region_id(self):
        for record in self:
            if record.region_id:
                city_ids = self.env['maintenance.city']. \
                    search([('region_id.id', '=', record.region_id.id)])
                cities = []
                for city in city_ids:
                    cities.append(city.id)
                domain = {'city_id': [('id', 'in', cities)]}
                return {'domain': domain}

    @api.onchange('city_id')
    def change_city_id(self):
        for record in self:
            if record.city_id:
                location_ids = self.env['maintenance.location']. \
                    search([('city_id.id', '=', record.city_id.id)])
                locations = []
                for location in location_ids:
                    locations.append(location.id)
                domain = {'location_id': [('id', 'in', locations)]}
                return {'domain': domain}

    @api.onchange('equipment_id')
    def change_equipment_id(self):
        for record in self:
            if record.equipment_id:
                if not record.category_id:
                    record.category_id = record.equipment_id.category_id
                if not record.location_id:
                    record.location_id = record.equipment_id.location_id
                if not record.city_id:
                    record.city_id = record.equipment_id.city_id
                if not record.region_id:
                    record.region_id = record.equipment_id.region_id

    @api.onchange('category_id')
    def change_category_id(self):
        for record in self:
            if record.category_id:
                maintenance_equipment_ids = self.env['maintenance.equipment']. \
                    search([('category_id.id', '=', record.category_id.id),
                            ('location_id.id', '=', record.location_id.id)])
                maintenances = []
                for main in maintenance_equipment_ids:
                    maintenances.append(main.id)
                domain = {'equipment_id': [('id', 'in', maintenances)]}
                return {'domain': domain}


class HelpdeskTicket(models.AbstractModel):
    _inherit = "helpdesk.ticket"

    @api.onchange('location_id')
    @api.depends('location_id.site_type_ids')
    def _get_categories_domain(self):
        category_list = []
        if self.location_id:
            if self.location_id.site_type_ids:
                category_list = self.location_id.site_type_ids.ids
        else:
            category_list = self.env['maintenance.equipment.category'].search([]).ids
        return {'domain': {'maintenance_equipment_category_id': [('id', 'in', category_list)]}}

    maintenance_equipment_id = fields.Many2one('maintenance.equipment', string='Site Name')
    maintenance_equipment_category_id = fields.Many2one('maintenance.equipment.category', string='Site Type',
                                                        domain=_get_categories_domain)
    team_id = fields.Many2one('helpdesk.team', string='CM Team')
    region_id = fields.Many2one('maintenance.region', required=1)
    city_id = fields.Many2one('maintenance.city', required=1)
    location_id = fields.Many2one('maintenance.location', required=1)

    @api.onchange('region_id')
    def change_region_id(self):
        for record in self:
            if record.region_id:
                city_ids = self.env['maintenance.city']. \
                    search([('region_id.id', '=', record.region_id.id)])
                cities = []
                for city in city_ids:
                    cities.append(city.id)
                domain = {'city_id': [('id', 'in', cities)]}
                return {'domain': domain}

    @api.onchange('city_id')
    def change_city_id(self):
        for record in self:
            if record.city_id:
                location_ids = self.env['maintenance.location']. \
                    search([('city_id.id', '=', record.city_id.id)])
                locations = []
                for location in location_ids:
                    locations.append(location.id)
                domain = {'location_id': [('id', 'in', locations)]}
                return {'domain': domain}

    @api.onchange('maintenance_equipment_category_id')
    def change_maintenance_equipment_category_id(self):
        for record in self:
            if record.maintenance_equipment_category_id:
                maintenance_equipment_ids = self.env['maintenance.equipment']. \
                    search([('category_id.id', '=', record.maintenance_equipment_category_id.id),
                            ('location_id.id', '=', record.location_id.id)])
                maintenances = []
                for main in maintenance_equipment_ids:
                    maintenances.append(main.id)
                domain = {'maintenance_equipment_id': [('id', 'in', maintenances)]}
                return {'domain': domain}

    @api.onchange('maintenance_equipment_id')
    def change_maintenance_equipment_id(self):
        for record in self:
            if record.maintenance_equipment_id:
                if not record.maintenance_equipment_category_id:
                    record.maintenance_equipment_category_id = record.maintenance_equipment_id.category_id
                if not record.location_id:
                    record.location_id = record.maintenance_equipment_id.location_id
                if not record.city_id:
                    record.city_id = record.maintenance_equipment_id.city_id
                if not record.region_id:
                    record.region_id = record.maintenance_equipment_id.region_id

    # @api.model
    # def create(self, values):
    #     # res = super(HelpdeskTicket, self).create(values)
    #     # values['maintenance_equipment_category_id'] = res.maintenance_equipment_id.category_id
    #     return super(HelpdeskTicket, self).create(values)
