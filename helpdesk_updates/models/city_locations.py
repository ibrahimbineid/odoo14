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


class MaintenanceRegion(models.Model):
    _name = "maintenance.region"

    name = fields.Char(required=1, String='Region')
    abbreviation = fields.Char()


class MaintenanceCity(models.Model):
    _name = "maintenance.city"

    name = fields.Char(required=1, String='City')
    abbreviation = fields.Char()
    region_id = fields.Many2one('maintenance.region', required=1)


class MaintenanceLocation(models.Model):
    _name = "maintenance.location"

    name = fields.Char(required=1, String='Location')
    abbreviation = fields.Char()
    region_id = fields.Many2one('maintenance.region', required=1)
    city_id = fields.Many2one('maintenance.city', required=1)
    site_type_ids = fields.Many2many('maintenance.equipment.category', required=1)

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
