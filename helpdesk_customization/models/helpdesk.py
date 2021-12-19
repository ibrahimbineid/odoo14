# -*- coding: utf-8 -*-


import datetime
from odoo import models, fields, api, _
from datetime import datetime


class AlarmType(models.Model):
    _name = 'alarm.type'
    _description = 'Alarm Type'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name')
    alarm_ids = fields.Many2many('helpdesk.ticket.type')


class HelpDeskInh(models.Model):
    _inherit = 'helpdesk.ticket'

    part_ids = fields.One2many('helpdesk.parts.line', 'ticket_id')
    ticket_ids = fields.Many2many('helpdesk.ticket.type')
    location_src_id = fields.Many2one('stock.location', required=True)
    location_dest_id = fields.Many2one('stock.location', required=True)
    material_ids = fields.One2many('material.line', 'helpdesk_ticket_id', related='maintenance_equipment_id.materials_lines')
    cctv_installed = fields.Many2many('product.product', 'name', 'uom_id',related='maintenance_equipment_id.cctv_installed')
    ptz_camera = fields.Many2one('product.product', related='maintenance_equipment_id.ptz_camera')
    contractor_name = fields.Many2one('res.partner', related='maintenance_equipment_id.contractor_name')
    site_contactor = fields.Many2one('contact.name', related='maintenance_equipment_id.site_contactor')
    no_of_ptz = fields.Many2many('product.product', 'type', 'barcode',related='maintenance_equipment_id.no_of_ptz')
    cctv_camera = fields.Many2one('product.product', related='maintenance_equipment_id.cctv_camera')
    ptz_contactor_name = fields.Many2one('res.partner', related='maintenance_equipment_id.ptz_contactor_name')
    ptz_site_name = fields.Many2one('contact.name', related='maintenance_equipment_id.ptz_site_name')
    no_of_fibre = fields.Many2many('product.product', 'default_code', 'categ_id' , related='maintenance_equipment_id.no_of_fibre')
    fibre_info = fields.Many2one('product.product', related='maintenance_equipment_id.fibre_info')
    fibre_contractor_name = fields.Many2one('res.partner', related='maintenance_equipment_id.fibre_contractor_name')
    fibre_site_name = fields.Many2one('contact.name', related='maintenance_equipment_id.fibre_site_name')
    ip_address = fields.Char('IP Address', related='maintenance_equipment_id.ip_address')
    cm_ref = fields.Char(string='Ticket Reference', copy=False, readonly=True, index=True, default=lambda self: _('New'))

    @api.model
    def create(self, vals):
        if vals.get('cm_ref', _('New')) == _('New'):
            vals['cm_ref'] = self.env['ir.sequence'].next_by_code('cm.ref') or _('New')
        result = super(HelpDeskInh, self).create(vals)
        return result
    
    counter_type = fields.Integer(default=0)
    review_stage = fields.Char(string="Revision Stage", readonly="TRUE")
    
    @api.onchange('stage_id')
    def onchange_stage_id(self):
        print('self')
        
    def write(self, vals):
        if self.stage_id.is_close:
            if self.counter_type == 0:
                vals['counter_type'] = 1
            elif self.counter_type > 0:
                vals['counter_type'] = self.counter_type + 1
            vals['review_stage'] = 'REV' + str(vals['counter_type'])
        return super(HelpDeskInh, self).write(vals)

    product_info_ids = fields.Many2many('product.product', 'currency_id', 'cost_currency_id', compute='compute_product_info')

    def compute_product_info(self):
        for rec in self:
            product_list = []
            for mt in rec.material_ids:
                product_list.append(mt.material_type.id)
            for line in rec.part_ids:
                if line.type == 'add':
                    product_list.append(line.product_id.id)
                if line.type == 'remove':
                    if line.product_id.id in product_list:
                        product_list.remove(line.product_id.id)
            rec.product_info_ids = product_list




    is_pole = fields.Boolean('Pole & Pole Foundation', related='maintenance_equipment_id.is_pole')
    is_outdoor = fields.Boolean('Outdoor Closures', related='maintenance_equipment_id.is_outdoor')
    is_battery = fields.Boolean('Battery Closures', related='maintenance_equipment_id.is_battery')
    is_civil = fields.Boolean('Civil & Fiber Network', related='maintenance_equipment_id.is_civil')
    is_optical = fields.Boolean('Optical Testing: Fiber Optical Length Measurement', related='maintenance_equipment_id.is_optical')
    is_attenuation = fields.Boolean('Optical Testing: Attenuation Test', related='maintenance_equipment_id.is_attenuation')
    is_camera = fields.Boolean('Cameras', related='maintenance_equipment_id.is_camera')
    is_site = fields.Boolean('Site Power', related='maintenance_equipment_id.is_site')
    is_wireless = fields.Boolean('Wireless System', related='maintenance_equipment_id.is_wireless')

    maintenance_equipment_id = fields.Many2one('maintenance.equipment')

    pole_lines = fields.One2many('pole.line', 'ticket_id')
    outdoor_lines = fields.One2many('outdoor.line', 'ticket_id')
    battery_lines = fields.One2many('battery.line', 'ticket_id')
    civil_lines = fields.One2many('civil.line', 'ticket_id')
    fibre_lines = fields.One2many('fibre.line', 'ticket_id')
    attenuation_lines = fields.One2many('attenuation.line', 'ticket_id')
    camera_lines = fields.One2many('camera.line', 'ticket_id')
    site_lines = fields.One2many('site.line', 'ticket_id')
    wireless_lines = fields.One2many('wireless.line', 'ticket_id')

    requirements_lines = fields.One2many('requirements.line', 'ticket_id')

    # pole_pic = fields.Binary('Attach Picture', related='maintenance_equipment_id.pole_pic')
    # outdoor_pic = fields.Binary('Attach Picture', related='maintenance_equipment_id.outdoor_pic')
    # battery_pic = fields.Binary('Attach Picture', related='maintenance_equipment_id.battery_pic')
    # civil_pic = fields.Binary('Attach Picture', related='maintenance_equipment_id.civil_pic')
    # fibre_pic = fields.Binary('Attach Picture', related='maintenance_equipment_id.fibre_pic')
    # attenuation_pic = fields.Binary('Attach Picture', related='maintenance_equipment_id.attenuation_pic')
    # camera_pic = fields.Binary('Attach Picture', related='maintenance_equipment_id.camera_pic')
    # site_pic = fields.Binary('Attach Picture', related='maintenance_equipment_id.site_pic')
    # wireless_pic = fields.Binary('Attach Picture', related='maintenance_equipment_id.wireless_pic')

    pole_pic = fields.Many2many('ir.attachment', 'res_model', related='maintenance_equipment_id.pole_pic')
    outdoor_pic = fields.Many2many('ir.attachment', 'file_size', related='maintenance_equipment_id.outdoor_pic')
    battery_pic = fields.Many2many('ir.attachment', 'url', related='maintenance_equipment_id.battery_pic')
    civil_pic = fields.Many2many('ir.attachment', 'name', related='maintenance_equipment_id.civil_pic')
    fibre_pic = fields.Many2many('ir.attachment', 'original_id', related='maintenance_equipment_id.fibre_pic')
    attenuation_pic = fields.Many2many('ir.attachment', 'res_id', related='maintenance_equipment_id.attenuation_pic')
    camera_pic = fields.Many2many('ir.attachment', 'res_name', related='maintenance_equipment_id.camera_pic')
    site_pic = fields.Many2many('ir.attachment', 'public', related='maintenance_equipment_id.site_pic')
    wireless_pic = fields.Many2many('ir.attachment', 'type', related='maintenance_equipment_id.wireless_pic')

    pole_comment = fields.Text('Comments', related='maintenance_equipment_id.pole_comment')
    outdoor_comment = fields.Text('Comments', related='maintenance_equipment_id.outdoor_comment')
    battery_comment = fields.Text('Comments', related='maintenance_equipment_id.battery_comment')
    civil_comment = fields.Text('Comments', related='maintenance_equipment_id.civil_comment')
    fibre_comment = fields.Text('Comments', related='maintenance_equipment_id.fibre_comment')
    attenuation_comment = fields.Text('Comments', related='maintenance_equipment_id.attenuation_comment')
    camera_comment = fields.Text('Comments', related='maintenance_equipment_id.camera_comment')
    site_comment = fields.Text('Comments', related='maintenance_equipment_id.site_comment')
    wireless_comment = fields.Text('Comments', related='maintenance_equipment_id.wireless_comment')

    # is_client_approved = fields.Boolean('Client Approved', tracking=True)
    # is_contractor_approved = fields.Boolean('Contractor Approved', tracking=True)
    #
    # def action_contractor_approve(self):
    #     self.is_contractor_approved = True
    #
    # def action_client_approve(self):
    #     self.is_client_approved = True

    is_pole_client_approved = fields.Boolean('Pole Client Approved', tracking=True)
    is_pole_contractor_approved = fields.Boolean('Pole Contractor Approved', tracking=True)

    is_outdoor_client_approved = fields.Boolean('Outdoor Client Approved', tracking=True)
    is_outdoor_contractor_approved = fields.Boolean('Outdoor Contractor Approved', tracking=True)

    is_battery_client_approved = fields.Boolean('Battery Client Approved', tracking=True)
    is_battery_contractor_approved = fields.Boolean('Battery Contractor Approved', tracking=True)

    is_civil_client_approved = fields.Boolean('Civil Client Approved', tracking=True)
    is_civil_contractor_approved = fields.Boolean('Civil Contractor Approved', tracking=True)

    is_fibre_client_approved = fields.Boolean('Fibre Client Approved', tracking=True)
    is_fibre_contractor_approved = fields.Boolean('Fibre Contractor Approved', tracking=True)

    is_attenuation_client_approved = fields.Boolean('Attenuation Client Approved', tracking=True)
    is_attenuation_contractor_approved = fields.Boolean('Attenuation Contractor Approved', tracking=True)

    is_camera_client_approved = fields.Boolean('Camera Client Approved', tracking=True)
    is_camera_contractor_approved = fields.Boolean('Camera Contractor Approved', tracking=True)

    is_site_client_approved = fields.Boolean('Site Client Approved', tracking=True)
    is_site_contractor_approved = fields.Boolean('Site Contractor Approved', tracking=True)

    is_wireless_client_approved = fields.Boolean('Wireless Client Approved', tracking=True)
    is_wireless_contractor_approved = fields.Boolean('Wireless Contractor Approved', tracking=True)

    pole_con_name = fields.Char('Contractor Pole Name')
    outdoor_con_name = fields.Char('Contractor Outdoor Name')
    battery_con_name = fields.Char('Contractor Battery Name')
    civil_con_name = fields.Char('Contractor Civil Name')
    fibre_con_name = fields.Char('Contractor Fibre Name')
    attenuation_con_name = fields.Char('Contractor Attenuation Name')
    camera_con_name = fields.Char('Contractor Camera Name')
    site_con_name = fields.Char('Contractor Site Name')
    wireless_con_name = fields.Char('Contractor wireless Name')

    pole_con_sig = fields.Char('Contractor Pole Signature')
    outdoor_con_sig = fields.Char('Contractor Outdoor Signature')
    battery_con_sig = fields.Char('Contractor Battery Signature')
    civil_con_sig = fields.Char('Contractor Civil Signature')
    fibre_con_sig = fields.Char('Contractor Fibre Signature')
    attenuation_con_sig = fields.Char('Contractor Attenuation Signature')
    camera_con_sig = fields.Char('Contractor Camera Signature')
    site_con_sig = fields.Char('Contractor Site Signature')
    wireless_con_sig = fields.Char('Contractor wireless Signature')

    pole_cl_name = fields.Char('Client Pole Name')
    outdoor_cl_name = fields.Char('Client  OutdoorName')
    battery_cl_name = fields.Char('Client Battery Name')
    civil_cl_name = fields.Char('Client Civil Name')
    fibre_cl_name = fields.Char('Client Fibre Name')
    attenuation_cl_name = fields.Char('Client Attenuation Name')
    camera_cl_name = fields.Char('Client Camera Name')
    site_cl_name = fields.Char('Client Site Name')
    wireless_cl_name = fields.Char('Client Wireless Name')

    pole_cl_sig = fields.Char('Client Pole Signature')
    outdoor_cl_sig = fields.Char('Client Outdoor Signature')
    battery_cl_sig = fields.Char('Client Battery Signature')
    civil_cl_sig = fields.Char('Client Civil Signature')
    fibre_cl_sig = fields.Char('Client Fibre Signature')
    attenuation_cl_sig = fields.Char('Client Attenuation Signature')
    camera_cl_sig = fields.Char('Client Camera Signature')
    site_cl_sig = fields.Char('Client Site Signature')
    wireless_cl_sig = fields.Char('Client Wireless Signature')

    @api.onchange('maintenance_equipment_id')
    def onchange_maintenance_equipment_id(self):
        self.action_is_pole()
        self.action_is_outdoor()
        self.action_is_battery()
        self.action_is_civil()
        self.action_is_fibre()
        self.action_is_attenuation()
        self.action_is_camera()
        self.action_is_site()
        self.action_is_wireless()

        # for rec in self.part_ids:
        #     rec.unlink()
        # for line in self.maintenance_equipment_id.transfer_id.move_ids_without_package:
        #     lines = {
        #         'type': 'add',
        #         'product_id': line.product_id.id,
        #         'name': line.product_id.name,
        #         'uom_id': line.product_id.uom_id.id,
        #         'qty': line.quantity_done,
        #         'ticket_id': self.id,
        #         'is_added': True,
        #     }
        #     line_list.append(lines)
        # stock_move = self.env['helpdesk.parts.line'].create(line_list)
        location = self.env['stock.location'].search([('name', '=', self.maintenance_equipment_id.name)], limit=1)
        location_src = self.env['stock.location'].search(
            [('name', '=', self.region_id.name), ('location_id.name', '=', 'WH')], limit=1)
        self.location_src_id = location_src.id
        self.location_dest_id = location.id
        if self.location_id:
            if self.location_id.site_type_ids:
                self.maintenance_equipment_category_id = self.location_id.site_type_ids[0].id

    def action_is_pole(self):
        pole_list = []
        if self.is_pole:
            if self.pole_lines:
                for line in self.pole_lines:
                    line.unlink()
            for rec in self.maintenance_equipment_id.pole_lines:
                pole_list.append((0, 0, {
                    'site_ins': rec.site_ins,
                }))
        self.pole_lines = pole_list

    def action_is_outdoor(self):
        pole_list = []
        if self.is_outdoor:
            if self.outdoor_lines:
                for line in self.outdoor_lines:
                    line.unlink()
            for rec in self.maintenance_equipment_id.outdoor_lines:
                pole_list.append((0, 0, {
                    'site_ins': rec.site_ins,
                }))
        self.outdoor_lines = pole_list

    def action_is_battery(self):
        pole_list = []
        if self.is_battery:

            if self.battery_lines:
                for line in self.battery_lines:
                    line.unlink()
            for rec in self.maintenance_equipment_id.outdoor_lines:
                pole_list.append((0, 0, {
                    'site_ins': rec.site_ins,
                }))
        self.battery_lines = pole_list

    def action_is_civil(self):
        pole_list = []
        if self.is_civil:
            if self.civil_lines:
                for line in self.civil_lines:
                    line.unlink()
            for rec in self.maintenance_equipment_id.civil_lines:
                pole_list.append((0, 0, {
                    'site_ins': rec.site_ins,
                }))
        self.civil_lines = pole_list

    def action_is_fibre(self):
        pole_list = []
        if self.is_optical:
            if self.fibre_lines:
                for line in self.fibre_lines:
                    line.unlink()
            # for rec in self.maintenance_equipment_id.fibre_lines:
            #     pole_list.append((0, 0, {
            #         'fif_nm': rec.fif_nm,
            #         'fif_nm_units': rec.fif_nm_units,
            #         'six_nm': rec.six_nm,
            #         'six_nm_units': rec.six_nm_units,
            #     }))
            for j in range(24):
                pole_list.append((0, 0, {
                    'fif_nm': '',
                    'fif_nm_units': '',
                    'six_nm': '',
                    'six_nm_units': '',
                }))
        self.fibre_lines = pole_list

    def action_is_attenuation(self):
        pole_list = []
        requirement_list = []
        if self.is_attenuation:
            if self.attenuation_lines:
                for line in self.attenuation_lines:
                    line.unlink()
            # for rec in self.maintenance_equipment_id.attenuation_lines:
            #     pole_list.append((0, 0, {
            #         'fif_nm_tx': rec.fif_nm_tx,
            #         'fif_nm_rx': rec.fif_nm_rx,
            #         'fif_nm_section': rec.fif_nm_section,
            #         'six_nm_tx': rec.six_nm_tx,
            #         'six_nm_rx': rec.six_nm_rx,
            #         'six_nm_section': rec.six_nm_section,
            #     }))
            for j in range(24):
                pole_list.append((0, 0, {
                    'fif_nm_tx': '',
                    'fif_nm_rx': '',
                    'fif_nm_section': '',
                    'six_nm_tx': '',
                    'six_nm_rx': '',
                    'six_nm_section': '',
                }))
            for line in self.maintenance_equipment_id.requirements_lines:
                requirement_list.append((0, 0, {
                    'requirement': line.requirement,
                    'fif_nm': '',
                    'six_nm': '',
                }))
        self.attenuation_lines = pole_list
        self.requirements_lines = requirement_list

    def action_is_camera(self):
        pole_list = []
        if self.is_camera:
            if self.camera_lines:
                for line in self.camera_lines:
                    line.unlink()
            for rec in self.maintenance_equipment_id.camera_lines:
                pole_list.append((0, 0, {
                    'site_ins': rec.site_ins,
                }))
        self.camera_lines = pole_list

    def action_is_site(self):
        pole_list = []
        if self.is_site:
            if self.site_lines:
                for line in self.site_lines:
                    line.unlink()
            for rec in self.maintenance_equipment_id.site_lines:
                pole_list.append((0, 0, {
                    'site_ins': rec.site_ins,
                }))
        self.site_lines = pole_list

    def action_is_wireless(self):
        pole_list = []
        if self.is_wireless:
            if self.wireless_lines:
                for line in self.wireless_lines:
                    line.unlink()
            for rec in self.maintenance_equipment_id.wireless_lines:
                pole_list.append((0, 0, {
                    'site_ins': rec.site_ins,
                }))
        self.wireless_lines = pole_list

    def action_pole_contractor_approve(self):
        self.pole_con_name = self.env.user.name
        self.is_pole_contractor_approved = True

    def action_pole_client_approve(self):
        self.pole_cl_name = self.env.user.name
        self.is_pole_client_approved = True

    def action_outdoor_contractor_approve(self):
        self.outdoor_con_name = self.env.user.name
        self.is_outdoor_contractor_approved = True

    def action_outdoor_client_approve(self):
        self.outdoor_cl_name = self.env.user.name
        self.is_outdoor_client_approved = True

    def action_battery_contractor_approve(self):
        self.battery_con_name = self.env.user.name
        self.is_battery_contractor_approved = True

    def action_battery_client_approve(self):
        self.battery_cl_name = self.env.user.name
        self.is_battery_client_approved = True

    def action_civil_contractor_approve(self):
        self.civil_con_name = self.env.user.name
        self.is_civil_contractor_approved = True

    def action_civil_client_approve(self):
        self.civil_cl_name = self.env.user.name
        self.is_civil_client_approved = True

    def action_fibre_contractor_approve(self):
        self.fibre_con_name = self.env.user.name
        self.is_fibre_contractor_approved = True

    def action_fibre_client_approve(self):
        self.fibre_cl_name = self.env.user.name
        self.is_fibre_client_approved = True

    def action_attenuation_contractor_approve(self):
        self.attenuation_con_name = self.env.user.name
        self.is_attenuation_contractor_approved = True

    def action_attenuation_client_approve(self):
        self.attenuation_cl_name = self.env.user.name
        self.is_attenuation_client_approved = True

    def action_camera_contractor_approve(self):
        self.camera_con_name = self.env.user.name
        self.is_camera_contractor_approved = True

    def action_camera_client_approve(self):
        self.camera_cl_name = self.env.user.name
        self.is_camera_client_approved = True

    def action_site_contractor_approve(self):
        self.site_con_name = self.env.user.name
        self.is_site_contractor_approved = True

    def action_site_client_approve(self):
        self.site_cl_name = self.env.user.name
        self.is_site_client_approved = True

    def action_wireless_contractor_approve(self):
        self.wireless_con_name = self.env.user.name
        self.is_wireless_contractor_approved = True

    def action_wireless_client_approve(self):
        self.wireless_cl_name = self.env.user.name
        self.is_wireless_client_approved = True

    def action_validate(self):
        for rec in self.part_ids:
            if not rec.is_picking_created:
                if rec.type == 'add' and not rec.is_added:
                    outgoing_pick = self.env['stock.picking.type'].search([('code', '=', 'outgoing')], limit=1)
                    source = ''
                    if rec.ticket_id:
                        source = rec.ticket_id.name
                    if rec.request_id:
                        source = rec.request_id.name
                    vals = {
                        'location_id': self.location_src_id.id,
                        'location_dest_id': self.location_dest_id.id,
                        'partner_id': self.partner_id.id,
                        'picking_type_id': outgoing_pick.id,
                        'scheduled_date': datetime.now(),
                        'move_type': 'direct',
                        'origin': source,
                    }
                    picking = self.env['stock.picking'].create(vals)
                    lines = {
                        'picking_id': picking.id,
                        'product_id': rec.product_id.id,
                        'name': rec.product_id.name,
                        'product_uom': rec.product_id.uom_id.id,
                        'location_id': self.location_src_id.id,
                        'location_dest_id': self.location_dest_id.id,
                        'product_uom_qty': rec.qty,
                    }
                    stock_move = self.env['stock.move'].create(lines)
                    picking.action_confirm()
                    rec.delivered_id = picking.id
                    rec.is_picking_created = True
                if rec.type == 'remove':
                    source = ''
                    if rec.ticket_id:
                        source = rec.ticket_id.name
                    if rec.request_id:
                        source = rec.request_id.name
                    incoming_pick = self.env['stock.picking.type'].search([('code', '=', 'incoming')], limit=1)
                    vals = {
                        'location_id': self.location_dest_id.id ,
                        'location_dest_id': self.location_src_id.id,
                        'partner_id': self.partner_id.id,
                        'picking_type_id': incoming_pick.id,
                        'scheduled_date': datetime.now(),
                        'move_type': 'direct',
                        'origin': source,
                    }
                    picking = self.env['stock.picking'].create(vals)
                    lines = {
                        'picking_id': picking.id,
                        'product_id': rec.product_id.id,
                        'name': rec.product_id.name,
                        'product_uom': rec.product_id.uom_id.id,
                        'location_id': self.location_dest_id.id ,
                        'location_dest_id': self.location_src_id.id,
                        'product_uom_qty': rec.qty,
                    }
                    stock_move = self.env['stock.move'].create(lines)
                    picking.action_confirm()
                    rec.received_id = picking.id
                    rec.is_picking_created = True


class HelpDeskPartsLine(models.Model):
    _name = 'helpdesk.parts.line'

    ticket_id = fields.Many2one('helpdesk.ticket')
    request_id = fields.Many2one('maintenance.request')
    type = fields.Selection([('add', 'Add'),
                                ('remove', 'Remove')], string='Type', required=True)
    product_id = fields.Many2one('product.product', required=True)
    name = fields.Char(related='product_id.name')
#     brand = fields.Many2one('stock.production.lot', domain="[('product_id', '=', product_id)]")
#     model = fields.Many2one('stock.production.lot', domain="[('product_id', '=', product_id)]")
    brand = fields.Many2one('product.brand')
    model = model = fields.Many2one('product.model')
    lot_id = fields.Many2one('stock.production.lot', domain="[('product_id', '=', product_id)]")
    # quant_id = fields.Many2one('stock.quant')
    qty = fields.Float('Qty')
    uom_id = fields.Many2one('uom.uom', related='product_id.uom_id')
    received_id = fields.Many2one('stock.picking')
    delivered_id = fields.Many2one('stock.picking')
    receive_qty = fields.Float(compute='compute_qty_done')
    delivered_qty = fields.Float(compute='compute_qty_done')
    is_picking_created = fields.Boolean()
    is_added = fields.Boolean(default=False)

    product_ids = fields.Many2many('product.product', 'currency_id', 'activity_type_id',
                                   compute='compute_products_added')

    @api.depends('type', 'request_id', 'ticket_id')
    def compute_products_added(self):
        for rec in self:
            product_list = []
            if rec.type:
                products = self.env['product.product'].search([])
                if rec.type == 'remove':
                    if rec.request_id:
                        rec.product_ids = rec.request_id.product_info_ids.ids
                    if rec.ticket_id:
                        rec.product_ids = rec.ticket_id.product_info_ids.ids
                else:
                    rec.product_ids = products.ids
            else:
                rec.product_ids = []

    def compute_qty_done(self):
        for rec in self:
            qty = 0
            if rec.received_id:
                for line in rec.received_id.move_line_ids_without_package:
                    qty = qty + line.qty_done
            if rec.delivered_id:
                for line in rec.delivered_id.move_line_ids_without_package:
                    qty = qty + line.qty_done
            rec.receive_qty = qty
            rec.delivered_qty = qty
            
    @api.onchange('product_id', 'brand')
    def onchange_product_id(self):
        for rec in self:
            if rec.type == 'add':
                if rec.product_id and rec.product_id.item_brands:
                    return {'domain': {'brand': [('id', 'in', rec.product_id.item_brands.ids)]}}
                else:
                    return {'domain': {'brand': [('id', 'in', [])]}}
            if rec.type == 'remove':
                if rec.request_id:
                    chkk = self.env['material.line'].search([('id', '=', self.request_id.material_ids.ids)])
                if rec.ticket_id:
                    chkk = self.env['material.line'].search([('id', '=', self.ticket_id.material_ids.ids)])
                loop = []
                for itm_id in chkk:
                    if rec.product_id == itm_id.material_type:
                        loop.append(itm_id.material_brand.id)
                return {'domain': {'brand': [('id', 'in', loop)]}}


    @api.onchange('brand', 'model')
    def onchange_brand(self):
        for rec in self:
            if rec.type == 'add':
                if rec.brand and rec.brand.model:
                    return {'domain': {'model': [('id', 'in', rec.brand.model.ids)]}}
                else:
                    return {'domain': {'model': [('id', 'in', [])]}}
            if rec.type == 'remove':
                if rec.request_id:
                    chkk = self.env['material.line'].search([('id', '=', self.request_id.material_ids.ids)])
                if rec.ticket_id:
                    chkk = self.env['material.line'].search([('id', '=', self.ticket_id.material_ids.ids)])
                loop = []
                for itm_id in chkk:
                    if rec.product_id == itm_id.material_type:
                        loop.append(itm_id.material_model.id)
                return {'domain': {'model': [('id', 'in', loop)]}}
