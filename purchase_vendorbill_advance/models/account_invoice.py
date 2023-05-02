# Copyright 2019-2022 Sodexis
# License OPL-1 (See LICENSE file for full copyright and licensing details)


from odoo import _, api, fields, models
from odoo.tools.float_utils import float_compare


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.model
    def _prepare_down_payment_section_line(self, **optional_values):
        """
        Prepare the dict of values to create a new down payment section for a sales order line.

        :param optional_values: any parameter that should be added to the returned down payment section
        """
        context = {'lang': self.partner_id.lang}
        down_payments_section_line = {
            'display_type': 'line_section',
            'name': _('Prepayments'),
            'product_id': False,
            'product_uom_id': False,
            'quantity': 0,
            'discount': 0,
            'price_unit': 0,
            'account_id': False
        }
        del context
        if optional_values:
            down_payments_section_line.update(optional_values)
        return down_payments_section_line

    @api.onchange("purchase_vendor_bill_id", "purchase_id")
    def _onchange_purchase_auto_complete(self):
        if not self.purchase_id and not self.purchase_vendor_bill_id:
            return
        company_id = self.purchase_id.company_id.id
        if self._context.get("final", False):
            if self.purchase_vendor_bill_id.vendor_bill_id:
                self.invoice_vendor_bill_id = (
                    self.purchase_vendor_bill_id.vendor_bill_id
                )
                self._onchange_invoice_vendor_bill()
            elif self.purchase_vendor_bill_id.purchase_order_id:
                self.purchase_id = self.purchase_vendor_bill_id.purchase_order_id

            if not self.purchase_id:
                return

            # Copy partner.
            self.partner_id = self.purchase_id.partner_id
            self.fiscal_position_id = self.purchase_id.fiscal_position_id
            self.invoice_payment_term_id = self.purchase_id.payment_term_id
            self.currency_id = self.purchase_id.currency_id

            new_lines = self.env["account.move.line"]
            precision = self.env["decimal.precision"].precision_get(
                "Product Unit of Measure"
            )

            down_payment_section_added = False
            initial_sequence = 10
           
            for line in self.purchase_id.order_line.sorted(lambda l: l.is_downpayment) - self.invoice_line_ids.mapped(
                "purchase_line_id"
            ):
                if not down_payment_section_added and line.is_downpayment:
                    downpayment_section_line_data = self._prepare_down_payment_section_line()
                    downpayment_section_line_data['sequence'] = initial_sequence + 1
                    downpayment_line = new_lines.new(downpayment_section_line_data)
                    new_lines += downpayment_line
                    down_payment_section_added = True
                if (
                    float_compare(
                        line.qty_invoiced,
                        line.product_qty
                        if line.product_id.purchase_method == "purchase"
                        else line.qty_received,
                        precision_digits=precision,
                    )
                    == -1
                    or line.is_downpayment
                    and line.qty_invoiced == 1
                ):
                    data = line._prepare_account_move_line(self)
                    data.update({
                        "move_id": self.id,
                        "currency_id": self.currency_id.id, # Mandatory field
                    })

                    if 'sequence' in data:
                        initial_sequence = data['sequence']
                    else:
                        data['sequence'] = initial_sequence + 1

                    new_line = new_lines.new(data)
                    new_lines += new_line
            # Compute invoice_origin.
            origins = set(new_lines.mapped("purchase_line_id.order_id.name"))
            self.invoice_origin = ",".join(list(origins))
            if any(line.purchase_line_id.is_downpayment for line in new_lines):
                downpayment_amount = 0.0
                other_line_amount = 0.0
                for line in new_lines:
                    if line.purchase_line_id.is_downpayment:
                        downpayment_amount += line.price_subtotal
                        line.quantity = -1
                    else:
                        other_line_amount += line.price_total
                if downpayment_amount > other_line_amount:
                    for line in new_lines:
                        if line.purchase_line_id.is_downpayment:
                            line.quantity = 1
                        else:
                            line.update({"quantity": -(line.quantity)})
                    self.env.context = dict(self.env.context)
                    self.env.context.update({"is_refund": True})
                    self.move_type = "in_refund"
            self.invoice_line_ids += new_lines
            # Compute ref.
            refs = set(self.line_ids.mapped("purchase_line_id.order_id.partner_ref"))
            refs = [ref for ref in refs if ref]
            self.ref = ",".join(refs)
            # Compute payment_reference. invoice_payment_ref
            if len(refs) == 1:
                self.payment_reference = refs[0]
            return {}
        elif self._context.get("without_downpayment", False):
            if self.purchase_vendor_bill_id.vendor_bill_id:
                self.invoice_vendor_bill_id = (
                    self.purchase_vendor_bill_id.vendor_bill_id
                )
                self._onchange_invoice_vendor_bill()
            elif self.purchase_vendor_bill_id.purchase_order_id:
                self.purchase_id = self.purchase_vendor_bill_id.purchase_order_id

            if not self.purchase_id:
                return

            # Copy partner.
            self.partner_id = self.purchase_id.partner_id
            self.fiscal_position_id = self.purchase_id.fiscal_position_id
            self.invoice_payment_term_id = self.purchase_id.payment_term_id
            self.currency_id = self.purchase_id.currency_id

            new_lines = self.env["account.move.line"]
            precision = self.env["decimal.precision"].precision_get(
                "Product Unit of Measure"
            )
            for line in (
                self.purchase_id.order_line
                - self.purchase_id.order_line.filtered(lambda x: x.is_downpayment)
            ):
                if (
                    float_compare(
                        line.qty_invoiced,
                        line.product_qty
                        if line.product_id.purchase_method == "purchase"
                        else line.qty_received,
                        precision_digits=precision,
                    )
                    == -1
                    or line.is_downpayment
                    and line.qty_invoiced == 1
                ):
                    data = line._prepare_account_move_line(self)
                    new_line = new_lines.new(data)
                    new_lines += new_line
            origins = set(new_lines.mapped("purchase_line_id.order_id.name"))
            self.invoice_origin = ",".join(list(origins))
            self.invoice_line_ids += new_lines
            # Compute ref.
            refs = set(self.line_ids.mapped("purchase_line_id.order_id.partner_ref"))
            refs = [ref for ref in refs if ref]
            self.ref = ",".join(refs)
            # Compute payment_reference.
            if len(refs) == 1:
                self.payment_reference = refs[0]
            return {}
        else:
            rec = super()._onchange_purchase_auto_complete()
            if not self.journal_id:
                self.update({'journal_id': self.env["account.journal"].search(
                [("type", "in", ["purchase"]), ("company_id", "=", company_id)], limit=1
                )})
            if not self.invoice_origin:
                self.invoice_origin = self.purchase_id.name
            return rec

    def unlink(self):
        downpayment_lines = self.mapped("invoice_line_ids.purchase_line_id").filtered(
            lambda line: line.is_downpayment
        )
        res = super(AccountMove, self).unlink()
        if downpayment_lines:
            downpayment_lines.unlink()
        return res


