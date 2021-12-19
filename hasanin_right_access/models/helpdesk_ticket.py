from odoo import api, models, _
from odoo.exceptions import UserError, ValidationError


class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    @api.model
    def create(self, values):
        if values.get('stage_id', False) and values['stage_id'] is int:
            stage_id = self.env['helpdesk.stage'].browse(values['stage_id'])

            # Check if the current user has access to change ticket to closed stage
            if stage_id.is_close:
                if not self.env.user.has_group('hasanin_right_access.can_move_to_closed_helpdesk_stages'):
                    raise UserError(_("You are not allowed to change ticket to closed stage !!"))

        return super(HelpdeskTicket, self).create(values)

    def write(self, values):

        stage_id = False
        if values.get('stage_id'):
            stage_id = self.env['helpdesk.stage'].browse(values['stage_id'])
        else:
            return super(HelpdeskTicket, self).write(values)

        # Check if the current user has access to change ticket to closed stage
        if stage_id.is_close:
            if not self.env.user.has_group('hasanin_right_access.can_move_to_closed_helpdesk_stages'):
                raise UserError(_("You are not allowed to change ticket to closed stage !!"))

        # Check if the current user has access to change ticket stage.
        if not stage_id.is_close:
            if not self.env.user.has_group('hasanin_right_access.can_move_btw_helpdesk_stages'):
                raise UserError(_("You are not allowed to change ticket stage !!"))

        return super(HelpdeskTicket, self).write(values)
