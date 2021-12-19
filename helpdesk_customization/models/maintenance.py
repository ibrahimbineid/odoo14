# -*- coding: utf-8 -*-


from odoo import models, fields, api, _


class MaintenanceEquipmentInherit(models.Model):
    _inherit = 'maintenance.equipment'

    materials_lines = fields.One2many('material.line', 'material_line_me_id')
    cctv_installed = fields.Many2many('product.product', 'taxes_id', 'uom_id')
    ptz_camera = fields.Many2one('product.product')
    contractor_name = fields.Many2one('res.partner')
    site_contactor = fields.Many2one('contact.name')
    no_of_ptz = fields.Many2many('product.product', 'tic_category_id', 'uom_po_id')
    cctv_camera = fields.Many2one('product.product')
    ptz_contactor_name = fields.Many2one('res.partner')
    ptz_site_name = fields.Many2one('contact.name')
    no_of_fibre = fields.Many2many('product.product', 'default_code', 'categ_id')
    fibre_info = fields.Many2one('product.product')
    fibre_contractor_name = fields.Many2one('res.partner')
    fibre_site_name = fields.Many2one('contact.name')
    ip_address = fields.Char('IP Address')

    product_ids = fields.Many2many('product.product', 'currency_id', 'activity_type_id', compute='compute_products_added')

    def compute_products_added(self):
        requests = self.env['maintenance.request'].search([('equipment_id', '=', self.id)])
        tickets = self.env['helpdesk.ticket'].search([('maintenance_equipment_id', '=', self.id)])
        product_list = []
        for request in requests:
            for request_line in request.part_ids:
                if request_line.type == 'add':
                    product_list.append(request_line.product_id.id)
        for ticket in tickets:
            for ticket_line in ticket.part_ids:
                if ticket_line.type == 'add':
                    product_list.append(ticket_line.product_id.id)
        self.product_ids = product_list

    is_pole = fields.Boolean('Pole & Pole Foundation')
    is_outdoor = fields.Boolean('Outdoor Closures')
    is_battery = fields.Boolean('Battery Closures')
    is_civil = fields.Boolean('Civil & Fiber Network')
    is_optical = fields.Boolean('Optical Testing: Fiber Optical Length Measurement')
    is_attenuation = fields.Boolean('Optical Testing: Attenuation Test')
    is_camera = fields.Boolean('Cameras')
    is_site = fields.Boolean('Site Power')
    is_wireless = fields.Boolean('Wireless System')

    pole_lines = fields.One2many('pole.line', 'pole_line_me_id')
    outdoor_lines = fields.One2many('outdoor.line', 'outdoor_line_em_id')
    battery_lines = fields.One2many('battery.line', 'battery_line_me_id')
    civil_lines = fields.One2many('civil.line', 'civil_line_me_id')
    fibre_lines = fields.One2many('fibre.line', 'fibre_line_me_id')
    attenuation_lines = fields.One2many('attenuation.line', 'attenuation_line_me_id')
    camera_lines = fields.One2many('camera.line', 'camera_line_me_id')
    site_lines = fields.One2many('site.line', 'site_line_me_id')
    wireless_lines = fields.One2many('wireless.line', 'wireless_line_me_id')

    requirements_lines = fields.One2many('requirements.line', 'requirements_line_me_id')

    site_type_id = fields.Many2one('site.type', required=True)
    site_group = fields.Many2one('site.group', required=True)
    site_code = fields.Char('Site Code')
    site_no = fields.Char('Site Number')
    site_assigned_to = fields.Date('Site Assigned To Date')
    # region = fields.Char('Region')
    # location = fields.Char('Location')
    # city = fields.Char('City')
    latitude = fields.Float('Latitude', digits=(16, 6))
    longitude = fields.Float('longitude', digits=(16, 6))
    transfer_id = fields.Many2many('stock.picking')

    pole_pic = fields.Many2many('ir.attachment','res_model')
    outdoor_pic = fields.Many2many('ir.attachment', 'file_size',)
    battery_pic = fields.Many2many('ir.attachment', 'url',)
    civil_pic = fields.Many2many('ir.attachment', 'name',)
    fibre_pic = fields.Many2many('ir.attachment', 'original_id',)
    attenuation_pic = fields.Many2many('ir.attachment', 'res_id',)
    camera_pic = fields.Many2many('ir.attachment', 'res_name',)
    site_pic = fields.Many2many('ir.attachment', 'public',)
    wireless_pic = fields.Many2many('ir.attachment', 'type',)

    pole_comment = fields.Text('Comments')
    outdoor_comment = fields.Text('Comments')
    battery_comment = fields.Text('Comments')
    civil_comment = fields.Text('Comments')
    fibre_comment = fields.Text('Comments')
    attenuation_comment = fields.Text('Comments')
    camera_comment = fields.Text('Comments')
    site_comment = fields.Text('Comments')
    wireless_comment = fields.Text('Comments')

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

    is_created = fields.Boolean()

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

    @api.onchange('location_id')
    def onchange_get_category(self):
        for rec in self:
            if rec.location_id.site_type_ids:
                rec.category_id = rec.location_id.site_type_ids[0].id

    @api.model
    def create(self, vals_list):
        record = super(MaintenanceEquipmentInherit, self).create(vals_list)
        if record.materials_lines:
            record.action_transfer_independent(record)
            record.is_created = True
        return record

    def action_transfer_independent(self, record):
        picking = self.env['stock.picking.type'].search([('code', '=', 'internal')], limit=1)
        wh = self.env['stock.location'].search([('name', '=', 'Stock')], limit=1)
        site_loc = self.env['stock.location'].search([('name', '=', record.location_id.name)], limit=1)
        new_loc = self.env['stock.location'].create({
            'name': record.name,
            'location_id': site_loc.id,
        })
        rec = self.env['stock.picking'].create({
            'partner_id': record.partner_id.id,
            'picking_type_id': picking.id,
            'location_id': wh.id,
            'location_dest_id': new_loc.id,
            'origin': record.name,
        })
        for m_installed in record.materials_lines:
            lines = self.env['stock.move.line'].create({
                'product_id': m_installed.material_type.id,
                'product_uom_qty': m_installed.material_qty,
                'product_uom_id': m_installed.material_type.uom_id.id,
                'location_id': wh.id,
                'location_dest_id': new_loc.id,
                'qty_done': m_installed.material_qty,
                'picking_id': rec.id,
            })
        record.transfer_id = [rec.id]

    def write(self, vals):
        if 'materials_lines' in vals:
            new_transfer = self.action_create_transfer(vals)
            vals['is_created'] = True
            transfer_list = []
            for tr in self.transfer_id:
                transfer_list.append(tr.id)
            transfer_list.append(new_transfer.id)
            vals['transfer_id'] = transfer_list
        else:
            print('not values')

        return super(MaintenanceEquipmentInherit, self).write(vals)

    def action_create_transfer(self, vals):
        # print(product_list)
        picking = self.env['stock.picking.type'].search([('code', '=', 'internal')], limit=1)
        wh = self.env['stock.location'].search([('name', '=', 'Stock')], limit=1)
        site_loc = self.env['stock.location'].search([('name', '=', self.name)], limit=1)
        if not site_loc:
            site_name = self.env['stock.location'].search([('name', '=', self.location_id.name)], limit=1)
            site_loc = self.env['stock.location'].create({
                'name': self.name,
                'location_id': site_name.id,
            })
        rec = self.env['stock.picking'].create({
            'partner_id': self.partner_id.id,
            'picking_type_id': picking.id,
            'location_id': wh.id,
            'location_dest_id': site_loc.id,
            'origin': self.name,
        })
        m_id = vals['materials_lines']
        y = []
        for x in range(len(m_id)):
            if not m_id[x][2] == False:
                y.append(m_id[x][2])
        for m_installed in y:
            material_uom = self.env['product.product'].search([('id', '=', m_installed['material_type'])])
            line = self.env['stock.move.line'].create({
                'product_id': m_installed['material_type'],
                'product_uom_qty': m_installed['material_qty'],
                'product_uom_id': material_uom.uom_id.id,
                'location_id': wh.id,
                'location_dest_id': site_loc.id,
                'qty_done': m_installed['material_qty'],
                'picking_id': rec.id,
            })
        return rec
        


    @api.onchange('is_pole')
    def onchange_is_pole(self):
        pole_list = []
        if self.is_pole:
            pole = self.env['alarm.type'].search([('name', '=', 'Pole & Pole Foundation')])
            if pole:
                for line in self.pole_lines:
                    line.unlink()
                for rec in pole.alarm_ids:
                    pole_list.append((0, 0, {
                        'site_ins': rec.name,
                    }))
        self.pole_lines = pole_list

    @api.onchange('is_outdoor')
    def onchange_is_outdoor(self):
        pole_list = []
        if self.is_outdoor:
            pole = self.env['alarm.type'].search([('name', '=', 'Outdoor Closures')])
            if pole:
                for line in self.outdoor_lines:
                    line.unlink()
                for rec in pole.alarm_ids:
                    pole_list.append((0, 0, {
                        'site_ins': rec.name,
                    }))
        self.outdoor_lines = pole_list

    @api.onchange('is_battery')
    def onchange_is_battery(self):
        pole_list = []
        if self.is_battery:
            pole = self.env['alarm.type'].search([('name', '=', 'Battery Closures')])
            if pole:
                for line in self.battery_lines:
                    line.unlink()
                for rec in pole.alarm_ids:
                    pole_list.append((0, 0, {
                        'site_ins': rec.name,
                    }))
        self.battery_lines = pole_list

    @api.onchange('is_civil')
    def onchange_is_civil(self):
        pole_list = []
        if self.is_civil:
            pole = self.env['alarm.type'].search([('name', '=', 'Civil & Fiber Network')])
            if pole:
                for line in self.civil_lines:
                    line.unlink()
                for rec in pole.alarm_ids:
                    pole_list.append((0, 0, {
                        'site_ins': rec.name,
                    }))
        self.civil_lines = pole_list

    @api.onchange('is_optical')
    def onchange_is_optical(self):
        pole_list = []
        if self.is_optical:
            pole = self.env['optical.test'].search([])
            if pole:
                i = 1
                for line in self.fibre_lines:
                    line.unlink()
                for rec in pole:
                    pole_list.append((0, 0, {
                        'fibre_no': i,
                        'fif_nm': rec.fif_nm,
                        'fif_nm_units': rec.fif_nm_units,
                        'six_nm': rec.six_nm,
                        'six_nm_units': rec.six_nm_units,
                    }))
                    i = i + 1
                f = len(pole_list)
                for j in range(24-f):
                    pole_list.append((0, 0, {
                        'fibre_no': i,
                        'fif_nm': '',
                        'fif_nm_units': '',
                        'six_nm': '',
                        'six_nm_units': '',
                    }))
                    i = i +1
            else:
                k = 1
                for j in range(24):
                    pole_list.append((0, 0, {
                        'fibre_no': k,
                        'fif_nm': '',
                        'fif_nm_units': '',
                        'six_nm': '',
                        'six_nm_units': '',
                    }))
                    k = k + 1
        self.fibre_lines = pole_list

    @api.onchange('is_attenuation')
    def onchange_is_attenuation(self):
        print("Hello")
        pole_list = []
        if self.is_attenuation:
            pole = self.env['attenuation.test'].search([])
            if pole:
                for line in self.attenuation_lines:
                    line.unlink()
                f = 1
                for rec in pole:
                    pole_list.append((0, 0, {
                        'fibre_no': f,
                        'fif_nm_tx': rec.fif_nm_tx,
                        'fif_nm_rx': rec.fif_nm_rx,
                        'fif_nm_section': rec.fif_nm_section,
                        'six_nm_tx': rec.six_nm_tx,
                        'six_nm_rx': rec.six_nm_rx,
                        'six_nm_section': rec.six_nm_section,
                    }))
                    f = f + 1
                i = len(pole_list)
                for j in range(24-i):
                    pole_list.append((0, 0, {
                        'fibre_no': f,
                        'fif_nm_tx': '',
                        'fif_nm_rx': '',
                        'fif_nm_section': '',
                        'six_nm_tx': '',
                        'six_nm_rx': '',
                        'six_nm_section': '',
                    }))
                    f = f + 1
            else:
                k = 1
                for j in range(24):
                    pole_list.append((0, 0, {
                        'fibre_no': k,
                        'fif_nm_tx': '',
                        'fif_nm_rx': '',
                        'fif_nm_section': '',
                        'six_nm_tx': '',
                        'six_nm_rx': '',
                        'six_nm_section': '',
                    }))
                    k = k + 1
        self.attenuation_lines = pole_list
        self.create_attenuation_requirements()

    def create_attenuation_requirements(self):
        pole_list = []
        if self.is_attenuation:
            pole = self.env['attenuation.requirements'].search([])
            if pole:
                for line in self.requirements_lines:
                    line.unlink()
                for rec in pole:
                    pole_list.append((0, 0, {
                        'requirement': rec.requirement,
                        'fif_nm': rec.fif_nm,
                        'six_nm': rec.six_nm,

                    }))
        self.requirements_lines = pole_list

    @api.onchange('is_camera')
    def onchange_is_camera(self):
        pole_list = []
        if self.is_camera:
            pole = self.env['alarm.type'].search([('name', '=', 'Cameras')])
            if pole:
                for line in self.camera_lines:
                    line.unlink()
                for rec in pole.alarm_ids:
                    pole_list.append((0, 0, {
                        'site_ins': rec.name,
                    }))
        self.camera_lines = pole_list

    @api.onchange('is_site')
    def onchange_is_site(self):
        pole_list = []
        if self.is_site:
            pole = self.env['alarm.type'].search([('name', '=', 'Site Power')])
            if pole:
                for line in self.site_lines:
                    line.unlink()
                for rec in pole.alarm_ids:
                    pole_list.append((0, 0, {
                        'site_ins': rec.name,
                    }))
        self.site_lines = pole_list

    @api.onchange('is_wireless')
    def onchange_is_wireless(self):
        pole_list = []
        if self.is_wireless:
            pole = self.env['alarm.type'].search([('name', '=', 'Wireless System')])
            if pole:
                for line in self.wireless_lines:
                    line.unlink()
                for rec in pole.alarm_ids:
                    pole_list.append((0, 0, {
                        'site_ins': rec.name,
                    }))
        self.wireless_lines = pole_list


class Material(models.Model):
    _name = 'material.line'

    material_line_me_id = fields.Many2one('maintenance.equipment')
    helpdesk_ticket_id = fields.Many2one('helpdesk.ticket')
    material_name = fields.Char(string='Name')
    material_type = fields.Many2one('product.product', string='Item Type')
    material_brand = fields.Many2one('product.brand', string='Brand')
    material_model = fields.Many2one('product.model', string='Model')
    material_qty = fields.Integer('Qty')
    material_serial_number = fields.Many2one('stock.production.lot', domain="[('product_id', '=', material_type)]", string='Serial Number')
    item_status = fields.Selection([('used', 'Used'), ('new', 'New')], string='Status')

    @api.onchange('material_type', 'material_brand')
    def onchange_material_type(self):
        for rec in self:
            if rec.material_type and rec.material_type.item_brands:
                return {'domain': {'material_brand': [('id', 'in', rec.material_type.item_brands.ids)]}}
            else:
                return {'domain': {'material_brand': [('id', 'in', [])]}}

    @api.onchange('material_brand', 'material_model')
    def onchange_material_brand(self):
        for rec in self:
            if rec.material_brand and rec.material_brand.model:
                return {'domain': {'material_model': [('id', 'in', rec.material_brand.model.ids)]}}
            else:
                return {'domain': {'material_model': [('id', 'in', [])]}}


class Pole(models.Model):
    _name = 'pole.line'

    pole_line_me_id = fields.Many2one('maintenance.equipment')
    ticket_id = fields.Many2one('helpdesk.ticket')
    request_id = fields.Many2one('maintenance.request')
    site_ins = fields.Char('Site Inspection')
    is_ok = fields.Boolean('Ok', default=False)
    is_not_ok = fields.Boolean('Not Ok', default=False)
    remarks = fields.Char('Remarks')

    @api.onchange('is_ok')
    def onchange_is_ok(self):
        if self.is_ok:
            self.is_not_ok = False

    @api.onchange('is_not_ok')
    def onchange_is_not_ok(self):
        if self.is_not_ok:
            self.is_ok = False


class OutDoor(models.Model):
    _name = 'outdoor.line'

    outdoor_line_em_id = fields.Many2one('maintenance.equipment')
    ticket_id = fields.Many2one('helpdesk.ticket')
    request_id = fields.Many2one('maintenance.request')
    site_ins = fields.Char('Site Inspection')
    is_ok = fields.Boolean('Ok')
    is_not_ok = fields.Boolean('Not Ok')
    remarks = fields.Char('Remarks')

    @api.onchange('is_ok')
    def onchange_is_ok(self):
        if self.is_ok:
            self.is_not_ok = False

    @api.onchange('is_not_ok')
    def onchange_is_not_ok(self):
        if self.is_not_ok:
            self.is_ok = False


class Battery(models.Model):
    _name = 'battery.line'

    site_ins = fields.Char('Site Inspection')
    is_ok = fields.Boolean('Ok')
    is_not_ok = fields.Boolean('Not Ok')
    remarks = fields.Char('Remarks')
    battery_line_me_id = fields.Many2one('maintenance.equipment')
    ticket_id = fields.Many2one('helpdesk.ticket')
    request_id = fields.Many2one('maintenance.request')

    @api.onchange('is_ok')
    def onchange_is_ok(self):
        if self.is_ok:
            self.is_not_ok = False

    @api.onchange('is_not_ok')
    def onchange_is_not_ok(self):
        if self.is_not_ok:
            self.is_ok = False


class Civil(models.Model):
    _name = 'civil.line'

    site_ins = fields.Char('Site Inspection')
    is_ok = fields.Boolean('Ok')
    is_not_ok = fields.Boolean('Not Ok')
    remarks = fields.Char('Remarks')
    civil_line_me_id = fields.Many2one('maintenance.equipment')
    ticket_id = fields.Many2one('helpdesk.ticket')
    request_id = fields.Many2one('maintenance.request')

    @api.onchange('is_ok')
    def onchange_is_ok(self):
        if self.is_ok:
            self.is_not_ok = False

    @api.onchange('is_not_ok')
    def onchange_is_not_ok(self):
        if self.is_not_ok:
            self.is_ok = False


class Fibre(models.Model):
    _name = 'fibre.line'

    # site_ins = fields.Char('Site Inspection')
    # is_ok = fields.Boolean('Ok')
    # is_not_ok = fields.Boolean('Not Ok')
    # remarks = fields.Char('Remarks')
    fibre_no = fields.Integer('Fibre No')
    fif_nm = fields.Char('1550nM')
    fif_nm_units = fields.Char('1550nM(Unit)')
    six_nm = fields.Char('1625nM')
    six_nm_units = fields.Char('1625nM(Units)')
    fibre_line_me_id = fields.Many2one('maintenance.equipment')
    ticket_id = fields.Many2one('helpdesk.ticket')
    request_id = fields.Many2one('maintenance.request')

    @api.depends('ticket_id', 'fibre_line_me_id', 'request_id')
    def _compute_fibre_no(self):
        # for rec in self:
        if self.ticket_id:
            for order in self.mapped('ticket_id'):
                number = 1
                for line in order.fibre_lines:
                    line.fibre_no = number
                    number += 1
        if self.fibre_line_me_id:
            for order in self.mapped('fibre_line_me_id'):
                number = 1
                for line in order.fibre_lines:
                    line.fibre_no = number
                    number += 1
        if self.request_id:
            for order in self.mapped('request_id'):
                number = 1
                for line in order.fibre_lines:
                    line.fibre_no = number
                    number += 1

    # @api.onchange('is_ok')
    # def onchange_is_ok(self):
    #     if self.is_ok:
    #         self.is_not_ok = False
    #
    # @api.onchange('is_not_ok')
    # def onchange_is_not_ok(self):
    #     if self.is_not_ok:
    #         self.is_ok = False


class Attenuation(models.Model):
    _name = 'attenuation.line'

    fibre_no = fields.Integer('Fibre No')
    fif_nm_tx = fields.Char('(1550nM) Tx(db)')
    fif_nm_rx = fields.Char('(1550nM) Rx(db)')
    fif_nm_section = fields.Char('(1550nM) Section Loss(db)')

    six_nm_tx = fields.Char('(1625nM) Tx(db)')
    six_nm_rx = fields.Char('(1625nM) Rx(db)')
    six_nm_section = fields.Char('(1625nM) Section Loss(db)')
    attenuation_line_me_id = fields.Many2one('maintenance.equipment')
    ticket_id = fields.Many2one('helpdesk.ticket')
    request_id = fields.Many2one('maintenance.request')

    @api.depends('ticket_id', 'attenuation_line_me_id', 'request_id')
    def _compute_fibre_no(self):
        # for rec in self:
            if self.ticket_id:
                for order in self.mapped('ticket_id'):
                    number = 1
                    for line in order.attenuation_lines:
                        line.fibre_no = number
                        number += 1
            if self.attenuation_line_me_id:
                for order in self.mapped('attenuation_line_me_id'):
                    number = 1
                    for line in order.attenuation_lines:
                        line.fibre_no = number
                        number += 1
            if self.request_id:
                for order in self.mapped('request_id'):
                    number = 1
                    for line in order.attenuation_lines:
                        line.fibre_no = number
                        number += 1


class Camera(models.Model):
    _name = 'camera.line'

    site_ins = fields.Char('Site Inspection')
    is_ok = fields.Boolean('Ok')
    is_not_ok = fields.Boolean('Not Ok')
    remarks = fields.Char('Remarks')
    camera_line_me_id = fields.Many2one('maintenance.equipment')
    ticket_id = fields.Many2one('helpdesk.ticket')
    request_id = fields.Many2one('maintenance.request')

    @api.onchange('is_ok')
    def onchange_is_ok(self):
        if self.is_ok:
            self.is_not_ok = False

    @api.onchange('is_not_ok')
    def onchange_is_not_ok(self):
        if self.is_not_ok:
            self.is_ok = False


class Site(models.Model):
    _name = 'site.line'

    site_ins = fields.Char('Site Inspection')
    is_ok = fields.Boolean('Ok')
    is_not_ok = fields.Boolean('Not Ok')
    remarks = fields.Char('Remarks')
    site_line_me_id = fields.Many2one('maintenance.equipment')
    ticket_id = fields.Many2one('helpdesk.ticket')
    request_id = fields.Many2one('maintenance.request')

    @api.onchange('is_ok')
    def onchange_is_ok(self):
        if self.is_ok:
            self.is_not_ok = False

    @api.onchange('is_not_ok')
    def onchange_is_not_ok(self):
        if self.is_not_ok:
            self.is_ok = False


class Wireless(models.Model):
    _name = 'wireless.line'

    site_ins = fields.Char('Site Inspection')
    is_ok = fields.Boolean('Ok')
    is_not_ok = fields.Boolean('Not Ok')
    remarks = fields.Char('Remarks')
    wireless_line_me_id = fields.Many2one('maintenance.equipment')
    ticket_id = fields.Many2one('helpdesk.ticket')
    request_id = fields.Many2one('maintenance.request')

    @api.model
    def create(self, vals):
        print("resssssssssssss", vals)
        res = super(Wireless, self).create(vals)
        print("resssssssssssss", res)
        return res

    def write(self, vals):
        if vals:
            print("writeeeeeeeeeeeee", vals)
        res = super(Wireless, self).write(vals)
        print("write after", res)
        return res

    @api.onchange('is_ok')
    def onchange_is_ok(self):
        if self.is_ok:
            self.is_not_ok = False

    @api.onchange('is_not_ok')
    def onchange_is_not_ok(self):
        if self.is_not_ok:
            self.is_ok = False


class RequirementsLines(models.Model):
    _name = 'requirements.line'

    requirement = fields.Char('Requirements')
    fif_nm = fields.Char('1550nm')
    six_nm = fields.Char('1625nm')
    requirements_line_me_id = fields.Many2one('maintenance.equipment')
    ticket_id = fields.Many2one('helpdesk.ticket')
    request_id = fields.Many2one('maintenance.request')
