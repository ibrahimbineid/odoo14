from odoo import models, fields, api, _


class AlarmType(models.Model):
    _name = 'site.type'

    name = fields.Char(string='Name')


class SiteGroup(models.Model):
    _name = 'site.group'

    name = fields.Char(string='Name')


class ContactName(models.Model):
    _name = 'contact.name'

    name = fields.Char(string='Name')


class MaintenanceLocationInh(models.Model):
    _inherit = "maintenance.location"

    site_id = fields.Many2one('maintenance.equipment')
    active = fields.Boolean("Active", default=True)


class OpticalTest(models.Model):
    _name = 'optical.test'
    _rec_name = 'fif_nm'

    fif_nm = fields.Char('1550nM')
    fif_nm_units = fields.Char('1550nM(Unit)')
    six_nm = fields.Char('1625nM')
    six_nm_units = fields.Char('1625nM(Units)')


class AttenuationTest(models.Model):
    _name = 'attenuation.test'
    _rec_name = 'fif_nm_tx'

    fif_nm_tx = fields.Char('(1550nM) Tx(db)')
    fif_nm_rx = fields.Char('(1550nM) Rx(db)')
    fif_nm_section = fields.Char('(1550nM) Section Loss(db)')

    six_nm_tx = fields.Char('(1625nM) Tx(db)')
    six_nm_rx = fields.Char('(1625nM) Rx(db)')
    six_nm_section = fields.Char('(1625nM) Section Loss(db)')


class AttenuationRequirements(models.Model):
    _name = 'attenuation.requirements'
    _rec_name = 'requirement'

    requirement = fields.Char('Requirement')
    fif_nm = fields.Char('1550nM')
    six_nm = fields.Char('1625nM')
