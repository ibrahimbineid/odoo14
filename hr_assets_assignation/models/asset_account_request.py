# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import UserError


class AssetAccountRequest(models.Model):
    _name = 'asset.account.request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "employee_id"

    def get_users(self, groupidxml):
        myuserlist = []
        groupid = self.env.ref(groupidxml).id
        groupObj = self.env['res.groups'].search([('id', '=', groupid)])
        if groupObj:
            for rec in groupObj.users:
                myuserlist.append(rec.id)
        return myuserlist

    def get_account_asset_assignation(self):
        asset_request_ids = self.search([('state', '=', 'assigned')]).mapped('asset_id').ids
        domain = [('state', '=', 'open'), ('id', 'not in', asset_request_ids)]
        return domain

    def get_employee_id(self):
        employee_id = self.env['hr.employee'].search([('user_id', '=', self.env.user.id)])
        if employee_id:
            return employee_id.id
        else:
            return False

    name = fields.Char()
    asset_request_description = fields.Char()
    asset_request_Reason = fields.Char()
    asset_request_startDate = fields.Date(default=fields.date.today())
    asset_request_deliveryDate= fields.Date()

    asset_request_Refuse_reason = fields.Char(string="Refuse Reason")
    refuse_boolean=fields.Boolean(default=False)
    employee_id = fields.Many2one('hr.employee', 'Employee', default=get_employee_id)
    type = fields.Selection([('asset', 'Asset'),
                             ('non_asset', 'Non Asset'),
                             ], default='asset', tracking=True)
    asset_id = fields.Many2one('account.asset', string="Asset Name", domain=get_account_asset_assignation)
    description = fields.Char(translate=True)
    type_of_disclaimer = fields.Selection([('vacation', 'Vacation'),
                                         ('final', 'Final'),
                                         ('both', 'Both'),
                                         ('at_specific_date', 'At Specific Date'),
                                         ], default='at_specific_date', tracking=True)
    date_of_asset_delivery = fields.Date(default=fields.date.today())
    date = fields.Date(default=fields.date.today())
    date_of_disclaimer = fields.Date('Date Of Clearance')
    is_disclaimer = fields.Boolean('Cleared')

    def _expand_states(self, states, domain, order):
        return [key for key, val in type(self).state.selection]

    state = fields.Selection([('draft', 'Draft'),
                              ('submit', 'Submitted'),
                              ('approve', 'In progress'),
                              ('assigned', 'Assigned'),
                              ('clearance', 'clearance'),
                              ('refuse', 'Refused'),
                              ], default='draft', tracking=True, group_expand='_expand_states')

    employee_asset_id = fields.Many2one('employee.assets')
    color = fields.Integer(compute="compute_color")
    state_of_asset_when_receive = fields.Char()
    state_of_asset_when_delivery = fields.Char()

    def _getdesc(self):
        value = dict(self.env['asset.account.request'].fields_get(allfields=['type'])['type']['selection'])
        for rec in self:
            if rec.type:
                rec.type_desc =value[rec.type]
            else:
                rec.type_desc = ''

    def _get_state_desc(self):
        value = dict(self.env['asset.account.request'].fields_get(allfields=['state'])['state']['selection'])

        for record in self:
            if record.state:
                record.state_desc = value[record.state]
            else:
                record.state_desc = ''

    def _get_type_of_disclaimer_desc(self):
        value = dict(self.env['asset.account.request'].fields_get(allfields=['type_of_disclaimer'])['type_of_disclaimer']['selection'])
        for record in self:
            if record.type_of_disclaimer:
                record.type_of_disclaimer_desc = value[record.type_of_disclaimer]
            else:
                record.type_of_disclaimer_desc = ''

    type_desc = fields.Char(compute="_getdesc")
    state_desc = fields.Char(compute="_get_state_desc")
    # state_seq = fields.Char(compute="_get_state_seq")
    type_of_disclaimer_desc = fields.Char(compute="_get_type_of_disclaimer_desc")
    car_employee_have= fields.Many2one('fleet.vehicle',string=_("Employee Car"),readonly=True )
    is_car = fields.Boolean("Car",default=False)



    def make_activity(self, user_ids):
        print("j...", user_ids)
        now = datetime.now()
        date_deadline = now.date()
        now = datetime.now()
        date_deadline = now.date()
        if self:
            if user_ids:
                actv_id = self.sudo().activity_schedule(
                    'mail.mail_activity_data_todo', date_deadline,
                    note=_(
                        '<a href="#" data-oe-model="%s" data-oe-id="%s">Task </a> for <a href="#" data-oe-model="%s" data-oe-id="%s">%s\'s</a> Review') % (
                             self._name, self.id, self.employee_id._name,
                             self.employee_id.id, self.employee_id.display_name),
                    user_id=user_ids,
                    res_id=self.id,

                    summary=_("Request Approve")
                )


    @api.model
    def create(self, values):
        values['name'] = self.env['ir.sequence'].next_by_code('asset.request.sequence')
        res = super(AssetAccountRequest, self).create(values)
        user_ids = res.mapped('employee_id.parent_id.user_id').ids or [self.env.uid]
        res.make_activity(user_ids[0])
        return res

    @api.depends('state')
    def compute_color(self):
        for record in self:
            if record.state == 'draft':
                record.color = 2
            elif record.state == 'assigned':
                record.color = 4
            else:
                record.color = 6
    def action_submit(self):
        user_ids = list(self.get_users("hr_assets_assignation.asset_assignation_approve_button"))
        print(user_ids)
        if user_ids:
            for rec in user_ids:
                self.make_activity(rec)
        self.state = 'submit'

    def action_approve(self):
        print("::::::::::::::::::", self.employee_id.name)
        user_ids = list(self.get_users("hr_assets_assignation.asset_assignation_assign_to_employee_button"))
        print(user_ids)
        if user_ids:
            for rec in user_ids:
                self.make_activity(rec)
        self.state = 'approve'

    def action_refuse(self):
        self.state = 'refuse'

    def action_assign_to_employee(self):
        self.state = 'assigned'

    def action_clearance(self):
        self.state = 'clearance'

    def set_to_draft(self):
        self.state = 'draft'

    @api.model
    def cron_check_asset_request_end_date(self):
        asset_obj = self.search([])
        for asset in asset_obj:
            if asset.type_of_disclaimer == 'at_specific_date':
                if asset.date_of_asset_delivery < fields.date.today() and asset.state == 'assigned':
                    print("::::::::::::::", asset.name, asset.date_of_asset_delivery)
                    user_ids = list(self.get_users("hr_assets_assignation.asset_assignation_clearance_button"))
                    if user_ids:
                        for rec in user_ids:
                            # self.make_cron_activity(rec, asset.id)
                            print("user_ids...", user_ids)
                            now = datetime.now()
                            date_deadline = now.date()
                            values = {
                                'res_id': asset.id,
                                'res_model_id': self.env['ir.model'].search(
                                    [('model', '=', 'asset.account.request')]).id,
                                'user_id': rec,
                                'summary': 'Asset Assignation',
                                'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                                'date_deadline': date_deadline
                            }
                            self.sudo().env['mail.activity'].create(values)


class CustodyRequestLine(models.Model):
    _name = 'employee.assets'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'employee_id'

    name = fields.Char()
    asset_account_ids = fields.One2many('employee.asset.line', 'employee_asset_id')
    employee_id = fields.Many2one('hr.employee', 'Employee')
    type_of_disclaimer = fields.Selection([('vacation', 'Vacation'),
                                           ('final', 'Final'),
                                           ('both', 'Both'),
                                           ], default='vacation', tracking=True)
    description = fields.Text()
    state = fields.Selection([('draft', 'Draft'),
                              ('first_approve', 'Request Sent'),
                              ('clearance', 'clearance'),
                              ], default='draft', tracking=True, )
    color = fields.Integer(compute="compute_color")

    @api.depends('state')
    def compute_color(self):
        for record in self:
            if record.state == 'draft':
                record.color = 2
            elif record.state == 'first_approve':
                record.color = 4
            elif record.state == 'clearance':
                record.color = 6
            else:
                record.color = 8

    def make_activity(self, user_ids):
        now = datetime.now()
        date_deadline = now.date()
        if self:
            if user_ids:
                actv_id = self.sudo().activity_schedule(
                    'mail.mail_activity_data_todo', date_deadline,
                    note=_(
                        '<a href="#" data-oe-model="%s" data-oe-id="%s">Task </a> for <a href="#" data-oe-model="%s" data-oe-id="%s">%s\'s</a> Review') % (
                             self._name, self.id, self.employee_id._name,
                             self.employee_id.id, self.employee_id.display_name),
                    user_id=user_ids,
                    res_id=self.id,

                    summary=_("Request Approve")
                )
                print("active", actv_id)

    @api.model
    def create(self, values):
        values['name'] = self.env['ir.sequence'].next_by_code('employee.assets.sequence')
        res = super(CustodyRequestLine, self).create(values)
        return res

    def action_first_approve(self):
        for record in self:
            items_need_disclaimer = record.asset_account_ids.filtered(lambda l: l.is_disclaimer == False)
            if len(items_need_disclaimer) >= len(record.asset_account_ids):
                raise UserError(_("You Must Select At Least One Asset To Approve"))
            record.state = 'first_approve'

    def action_clearance(self):
        self.state = 'clearance'

    def action_done(self):
        self.state = 'done'

    def set_to_draft(self):
        self.state = 'draft'

    @api.onchange('employee_id', 'type_of_disclaimer')
    def onchange_employee_id(self):
        print("111111111111111111")
        self.asset_account_ids = False
        if self.employee_id:
            asset_account_obj = self.env['asset.account.request'].search([('employee_id.id', '=', self.employee_id.id),
                                                                          ('state', '=', 'assigned'),
                                                                          ('type_of_disclaimer', '=', self.type_of_disclaimer)])
            print("employee_id", self.employee_id.id)
            print("self.type_of_disclaimer", self.type_of_disclaimer)
            print("1111111111dd11111111", asset_account_obj)
            if asset_account_obj:
                for line in asset_account_obj:
                    self.asset_account_ids.new({
                        'employee_asset_id': self.id,
                        'employee_id': line.employee_id,
                        'custody_request_id': line.id,
                        'type': line.type,
                        'asset_id': line.asset_id.id,
                        'description': line.description,
                        'date': line.date,
                    })

    def get_day_name_from_date(self, contract_day):
        contract_day = str(contract_day)
        year, month, day = contract_day.split('-')
        print(year, month, day)
        day_name = datetime(int(year), int(month), int(day))
        # day_name = date(int(year), int(month), int(day))
        e_name = day_name.strftime("%A")
        if e_name == 'Saturday':
            ar_name = 'السبت'
        elif e_name == 'Sunday':
            ar_name = 'الاحد'
        elif e_name == 'Monday':
            ar_name = 'الاثنين'
        elif e_name == 'Tuesday':
            ar_name = 'الثلاثاء'
        elif e_name == 'Wednesday':
            ar_name = 'الاربعاء'
        elif e_name == 'Thursday':
            ar_name = 'الخميس'
        else:
            ar_name = 'الجمعه'
        return ar_name


class EmployeeAssetLine(models.Model):
    _name = 'employee.asset.line'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "employee_id"

    custody_request_id = fields.Many2one('asset.account.request')
    employee_id = fields.Many2one('hr.employee', 'Employee')
    type = fields.Selection([('asset', 'Asset'),
                             ('non_asset', 'Non Asset'),
                             ], default='asset', tracking=True)
    asset_id = fields.Many2one('account.asset')
    description = fields.Char()
    type_of_disclaimer = fields.Selection([('vacation', 'Vacation'),
                             ('final', 'Final'),
                             ('both', 'Both'),
                             ], default='vacation', tracking=True)
    date = fields.Date(default=fields.date.today(), string='Assignation Date')
    date_of_disclaimer = fields.Date('Date Of Clearance')
    is_disclaimer = fields.Boolean('Cleared')
    employee_asset_id = fields.Many2one('employee.assets')


class DepartmentClearance(models.Model):
    _name = 'department.clearance'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'employee_id'

    department_clearance_line_ids = fields.One2many('department.clearance.line', 'department_clearance_id')
    employee_id = fields.Many2one('hr.employee', 'Employee')

    @api.onchange('employee_id')
    def onchange_employee_id(self):
        self.department_clearance_line_ids = False
        if self.employee_id:
            department_obj = self.env['hr.department'].search([])
            if department_obj:
                for line in department_obj:
                    self.department_clearance_line_ids.new({
                        'department_clearance_id': self.id,
                        'department_id': line.id,
                        'department_manager_id': line.manager_id.id,
                    })

    def get_day_name_from_date(self, contract_day):
        contract_day = str(contract_day)
        year, month, day = contract_day.split('-')
        # day_name = datetime.date(int(year), int(month), int(day))
        day_name = datetime(int(year), int(month), int(day))
        e_name = day_name.strftime("%A")
        if e_name == 'Saturday':
            ar_name = 'السبت'
        elif e_name == 'Sunday':
            ar_name = 'الاحد'
        elif e_name == 'Monday':
            ar_name = 'الاثنين'
        elif e_name == 'Tuesday':
            ar_name = 'الثلاثاء'
        elif e_name == 'Wednesday':
            ar_name = 'الاربعاء'
        elif e_name == 'Thursday':
            ar_name = 'الخميس'
        else:
            ar_name = 'الجمعه'
        return ar_name


class DepartmentClearanceLine(models.Model):
    _name = 'department.clearance.line'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    department_clearance_id = fields.Many2one('department.clearance')
    department_id = fields.Many2one('hr.department', 'Department Name')
    department_manager_id = fields.Many2one('hr.employee')
    notes = fields.Char()
    signature = fields.Char()
    date = fields.Date('Clearance Date', default=fields.date.today())
    is_department_manager = fields.Boolean(compute="compute_is_department_manager")

    @api.onchange('department_id')
    def onchange_department_id(self):
        for record in self:
            record.department_manager_id = record.department_id.manager_id.id

    @api.depends('department_manager_id')
    def compute_is_department_manager(self):
        for record in self:
            current_user_id = self.env['hr.employee'].search([('user_id', '=', self.env.user.id)])
            if current_user_id:
                if current_user_id.department_id and current_user_id.department_id.manager_id:
                    if record.department_manager_id.id == current_user_id.department_id.manager_id.id:
                        record.is_department_manager = True
                    else:
                        record.is_department_manager = False
                else:
                    record.is_department_manager = False
            else:
                record.is_department_manager = False
