from odoo import api, fields, models, _


class HrDirection(models.Model):
    _name = 'hr.direction'
    name = fields.Char()


class Contract(models.Model):
    _inherit = 'hr.contract'

    home_allowance = fields.Float()
    transportation_allowance = fields.Float()
    mobile_allowance = fields.Float()
    other_allowance = fields.Float()
    deduct_tamenat = fields.Boolean()
    tameenat_deduction = fields.Float(compute='get_tameenat_deduction', store=True)
    total_salary = fields.Float(compute='get_total_salary', store=True)
    net_contract_salary = fields.Float(compute='get_net_contract_salary', store=True)
    direction_id = fields.Many2one('hr.direction', string='Direction needed')

    @api.depends('wage', 'home_allowance', 'transportation_allowance', 'mobile_allowance', 'other_allowance')
    def get_total_salary(self):
        for record in self:
            allowances = record.home_allowance+record.transportation_allowance+record.mobile_allowance+record.other_allowance
            record.total_salary = record.wage+allowances

    @api.depends('deduct_tamenat', 'wage', 'home_allowance')
    def get_tameenat_deduction(self):
        for record in self:
            if record.deduct_tamenat:
                record.tameenat_deduction = ((record.wage + record.home_allowance)*10)/100
            else:
                record.tameenat_deduction = 0.0

    @api.depends('total_salary', 'tameenat_deduction')
    def get_net_contract_salary(self):
        for record in self:
            record.net_contract_salary = record.total_salary - record.tameenat_deduction
