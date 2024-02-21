# Copyright 2022      Eezee-IT (<http://www.eezee-it.com>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import api, fields, models, _
from odoo.addons.mail.wizard.mail_compose_message import _reopen
from odoo.exceptions import UserError
from odoo.tools.misc import get_lang


class BioNominationSend(models.TransientModel):
    _name = 'bio.nomination.send'
    _inherits = {'mail.compose.message': 'composer_id'}
    _description = 'Nomination Send'

    nomination_ids = fields.Many2many(
        'bio.nomination', 'bio_nomination_send_rel', string='Nominations')
    composer_id = fields.Many2one(
        'mail.compose.message', string='Composer',
        required=True, ondelete='cascade')
    template_id = fields.Many2one(
        'mail.template', 'Use template', index=True,
        domain="[('model', '=', 'bio.nomination')]"
        )

    @api.model
    def default_get(self, fields):
        res = super(BioNominationSend, self).default_get(fields)
        res_ids = self._context.get('active_ids')

        nominations = self.env['bio.nomination'].browse(res_ids)
        if not nominations:
            raise UserError(_("You can only send nominations."))

        composer = self.env['mail.compose.message'].create({
            'composition_mode': 'comment' if len(res_ids) == 1 else 'mass_mail',
        })
        res.update({
            'nomination_ids': res_ids,
            'composer_id': composer.id,
        })
        return res

    @api.onchange('nomination_ids')
    def _compute_composition_mode(self):
        for wizard in self:
            wizard.composer_id.composition_mode = 'comment' if len(
                wizard.nomination_ids) == 1 else 'mass_mail'

    @api.onchange('template_id')
    def onchange_template_id(self):
        for wizard in self:
            if wizard.composer_id:
                wizard.composer_id.template_id = wizard.template_id.id
                wizard._compute_composition_mode()
                wizard.composer_id._onchange_template_id_wrapper()

    def _send_email(self):
        user = self.env.user
        self.composer_id.with_context(
            mail_notify_author=user.partner_id in self.composer_id.partner_ids,
            mailing_document_based=True)._action_send_mail()

    def send_action(self):
        self.ensure_one()
        if self.composition_mode == 'mass_mail' and self.template_id:
            active_ids = self.env.context.get('active_ids', self.res_id)
            active_records = self.env[self.model].browse(active_ids)
            langs = active_records.mapped('partner_id.lang')
            default_lang = get_lang(self.env)
            for lang in (set(langs) or [default_lang]):
                active_ids_lang = active_records.filtered(
                    lambda r: r.partner_id.lang == lang).ids
                self_lang = self.with_context(
                    active_ids=active_ids_lang, lang=lang)
                self_lang.onchange_template_id()
                self_lang._send_email()
        else:
            self._send_email()

        return {'type': 'ir.actions.act_window_close'}

    def save_as_template(self):
        self.ensure_one()
        self.composer_id.action_save_as_template()
        self.template_id = self.composer_id.template_id.id
        action = _reopen(self, self.id, self.model, context=self._context)
        action.update({'name': _('Send Nomination')})
        return action
