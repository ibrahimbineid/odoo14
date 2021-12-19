
from odoo import models, fields, api, _


class PetrolSite(models.Model):
    _name = 'petrolling.site'
    _rec_name = 'ref_name'

    ref_name = fields.Char('Reference Name', copy=False, required=True, readonly=True,
        default=lambda self: self.env['ir.sequence'].next_by_code('patrolling.sequences'))
    site_group_id = fields.Many2one('site.group')
    site_id = fields.Many2many('maintenance.equipment')
    date = fields.Datetime('Date', default=lambda self: fields.Datetime.now())
    user_id = fields.Many2one('res.users', default=lambda self: self.env.user.id)
    employee_id = fields.Many2one('hr.employee', default=lambda self: self.env.user.employee_id.id)
    sites_region = fields.Many2one('maintenance.region', string='Region')
    petrol_lines = fields.One2many('petrolling.site.line', 'petrol_id')
    ck_status = fields.Boolean('Status')


    @api.onchange('site_group_id')
    def onchange_site_group_id(self):
        if self.site_group_id:
            site_list = []
            sites = self.env['maintenance.equipment'].search([('site_group', '=', self.site_group_id.id)])
            if sites:
                for rec in sites:
                    site_list.append(rec.id)
                self.sites_region = sites.region_id.id
            self.site_id = [(6, 0, site_list)]
           

#     @api.onchange('site_id')
#     def onchange_site_id(self):
#         if self.site_id:
#             alarm_list = []
#             alarm = self.env['alarm.type'].search([])
#             opticals = self.env['optical.test'].search([])
#             attenuations = self.env['attenuation.test'].search([])
#             if alarm:
#                 for line in self.petrol_lines:
#                     line.unlink()
#                 for rec in alarm:
#                     alarm_list.append((0, 0, {
#                         'alarm_name': rec.name,
#                     }))
#                 # for optical in opticals:
#                 #     alarm_list.append((0, 0, {
#                 #         'alarm_name': rec.name,
#                 #     }))
#                 self.petrol_lines = alarm_list


class PetrolSiteLine(models.Model):
    _name = 'petrolling.site.line'

    petrol_id = fields.Many2one('petrolling.site')
    alarm_name = fields.Char('Components')
#     status = fields.Boolean('Status')
    action = fields.Char('Action')
    issue = fields.Char('Issue')
    image = fields.Binary('Attachment')

