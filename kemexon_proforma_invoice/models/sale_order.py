from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    proforma_invoice_ids = fields.One2many(
        comodel_name='proforma.invoice',
        inverse_name='sale_order_id',
        string='Pro-forma Invoices',
    )

    proforma_invoice_count = fields.Integer(
        string='Pro-forma Invoice Count',
        compute='_compute_proforma_invoice_count',
    )

    @api.depends('proforma_invoice_ids')
    def _compute_proforma_invoice_count(self):
        for order in self:
            order.proforma_invoice_count = len(order.proforma_invoice_ids)

    def create_proforma_invoice(self):
        proforma_invoice_values = {
            'sale_order_id': self.id,
            'name': self.name,
            'partner_id': self.partner_id.id,
        }

        proforma_invoice = self.env['proforma.invoice'].create(proforma_invoice_values)

        proforma_invoice_line = []
        for sale_order_line in self.order_line:
            proforma_invoice_line_values = {
                'proforma_invoice_ids': proforma_invoice.id,
                'sale_order_line_id': sale_order_line.id,
            }
            proforma_invoice_line.append((0, 0, proforma_invoice_line_values))

        proforma_invoice.proforma_invoice_line_ids = proforma_invoice_line
        return {
            'name': 'Pro-forma Invoice',
            'type': 'ir.actions.act_window',
            'res_model': 'proforma.invoice',
            'res_id': proforma_invoice.id,
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'current',
        }

    def action_view_proforma_invoice(self):
        # Replace 'proforma.invoice' with your actual model name
        proforma_invoices = self.mapped('proforma_invoice_ids')

        # action = self.env['ir.actions.act_window']._for_xml_id('kemexon_proforma_invoice.view_proforma_invoice_form')
        action = {
            'name': 'Pro-forma Invoice',
            'type': 'ir.actions.act_window',
            'res_model': 'proforma.invoice',
            'view_mode': 'tree,form',
            'view_type': 'tree,form',
            'target': 'current',
        }

        if len(proforma_invoices) > 1:
            action['domain'] = [('id', 'in', proforma_invoices.ids)]
        elif len(proforma_invoices) == 1:
            form_view = [(self.env.ref('kemexon_proforma_invoice.view_proforma_invoice_form').id, 'form')]

            if 'views' in action:
                action['views'] = form_view + [(state, view) for state, view in action['views'] if view != 'form']
            else:
                action['views'] = form_view

            action['res_id'] = proforma_invoices[0].id  # Use the ID of the first proforma invoice
        else:
            action = {'type': 'ir.actions.act_window_close'}

        context = {
            # You can add default context values here
        }

        if len(self) == 1:
            context.update({
                # Add default context values specific to your use case
            })

        action['context'] = context
        return action


