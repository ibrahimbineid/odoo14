from odoo import models, api


class MaintenanceLocationInh(models.Model):
    _inherit = 'maintenance.location'

    @api.model
    def create(self, vals_list):
        record = super(MaintenanceLocationInh, self).create(vals_list)
        wh = self.env['stock.location'].search([('name', '=', 'SITE')], limit=1)
        region = self.env['stock.location'].search([('name', '=', record.region_id.name)], limit=1)
        if not region:
            region_vals = {
                'name': record.region_id.name,
                'usage': 'internal',
                'location_id': wh.id,
            }
            region = self.env['stock.location'].create(region_vals)
        city = self.env['stock.location'].search([('name', '=', record.city_id.name)], limit=1)
        if not city:
            city_vals = {
                'name': record.city_id.name,
                'usage': 'internal',
                'location_id': region.id,
            }
            city = self.env['stock.location'].create(city_vals)
        vals = {
            'name': record.name,
            'usage': 'internal',
            'location_id': city.id,
        }
        rec = self.env['stock.location'].create(vals)
        return record
