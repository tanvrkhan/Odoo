from odoo import api, fields, models, _
from odoo.exceptions import Warning


class WkWizardMessage(models.TransientModel):
    _name = "wk.wizard.message"
    _description = "Message Wizard"

    text = fields.Text(string='Message')

    @api.model
    def genrated_message(self, message, name='Message/Summary'):
        res = self.create({'text': message})
        return {
            'name': name,
            'type': 'ir.actions.act_window',
            'res_model': 'wk.wizard.message',
            'view_mode': 'form',
            'target': 'new',
            'res_id': res.id,
        }

    def allow_validation(self):
        relate_delivery = self.env['stock.picking'].browse(self.env.context.get('delivery_id'))
        return relate_delivery.with_context(check_condition=0).button_validate()
