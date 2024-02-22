# -*- coding: utf-8 -*-
# Copyright 2023 Eezee-IT (<http://www.eezee-it.com>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class AccountMove(models.Model):
    _inherit = 'account.move'

    deal_reference = fields.Char("Deal Ref")

    @api.constrains('ref', 'move_type', 'partner_id', 'journal_id', 'state')
    def _check_duplicate_supplier_reference(self):
        moves = \
            self.filtered(lambda mo: mo.state == 'posted' and mo.ref and mo.is_purchase_document())

        if not moves:
            return

        self.env["account.move"].flush([
            "ref", "move_type", "journal_id",
            "company_id", "partner_id", "commercial_partner_id",
        ])
        self.env["account.journal"].flush(["company_id"])
        self.env["res.partner"].flush(["commercial_partner_id"])

        # /!\ Computed stored fields are not yet inside the database.
        self._cr.execute('''
            SELECT move2.id
            FROM account_move move
            JOIN account_journal journal ON journal.id = move.journal_id
            JOIN res_partner partner ON partner.id = move.partner_id
            INNER JOIN account_move move2 ON
                move2.ref = move.ref
                AND move2.company_id = journal.company_id
                AND move2.commercial_partner_id = partner.commercial_partner_id
                AND move2.move_type = move.move_type
                AND move2.id != move.id
            WHERE move.id IN %s
        ''', [tuple(moves.ids)])
        duplicated_moves = self.browse([r[0] for r in self._cr.fetchall()])
        if duplicated_moves:
            raise ValidationError(_('Duplicated vendor reference detected. '
                                    'You probably encoded twice the same '
                                    'vendor bill/credit '
                                    'note:\n%s') % "\n".join(
                duplicated_moves.mapped(lambda m: "%(partner)s - %(ref)s" % {
                    'ref': m.ref,
                    'partner': m.partner_id.display_name
                })
            ))

    def _get_delivery_address(self):
        if self and self.invoice_line_ids:
            if self.invoice_line_ids.mapped('sale_line_ids'):
                if self.invoice_line_ids.sale_line_ids.move_ids.\
                        filtered(lambda x: x.state != 'cancel'):
                    return self.invoice_line_ids.sale_line_ids.move_ids. \
                        filtered(lambda x: x.state != 'cancel')[0].partner_id
        return

    def _get_delivery_date(self):
        if self and self.invoice_line_ids:
            if self.invoice_line_ids.mapped('sale_line_ids'):
                if self.invoice_line_ids.sale_line_ids.move_ids.\
                        filtered(lambda x: x.state != 'cancel'):
                    return self.invoice_line_ids.sale_line_ids.move_ids. \
                        filtered(lambda x: x.state != 'cancel')[0].\
                        picking_id.scheduled_date
        return
