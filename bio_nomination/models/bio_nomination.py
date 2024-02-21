# Copyright 2022      Eezee-IT (<http://www.eezee-it.com>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import fields, models, api, _
from odoo.tools.misc import get_lang


class BioNomination(models.Model):
    _name = "bio.nomination"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Bio Nomination"

    @api.onchange('purchase_id', 'sale_id')
    def _onchange_purchase_sale(self):
        self.nomination_lines = False
        if self.type in ('purchase_vessels', 'purchase_trucks') and self.purchase_id:
            self.partner_id = self.purchase_id.partner_id.id
            self.freight_charges = self.purchase_id.incoterm_id.id
            self.origin = self.pickup_place = self.purchase_id.origin_country_id.name
            self.origin_state = self.purchase_id.origin_state_id.name
            self.destination = self.purchase_id.dest_address_id.name or self.purchase_id.picking_type_id.display_name
            self.contract_ref = self.purchase_id.partner_ref
            self.laycan_to = self.purchase_id.laycan_to
            self.laycan_from = self.purchase_id.laycan_from
            self.picking_ids = self.purchase_id.picking_ids.ids
            self.nomination_lines = [(0, 0, {'product_id': line.product_id, 'qty': line.product_qty,
                                             'qty_done': line.product_qty,
                                             'product_packaging_id': line.product_packaging_id.id,
                                             'product_packaging_qty': line.product_packaging_qty}
                                      ) for line in self.purchase_id.order_line]
            product_ids = self.purchase_id.order_line.filtered(lambda o: o.product_id.detailed_type == 'product')
            self.account_analytic_id = product_ids and product_ids[0].account_analytic_id.id or False
        elif self.sale_id and self.type in ('sale_vessels', 'sale_trucks'):
            self.partner_id = self.sale_id.partner_id.id
            self.freight_charges = self.sale_id.incoterm.id
            self.origin = self.pickup_place = self.sale_id.origin_country_id.name
            self.origin_state = self.sale_id.origin_state_id.name
            self.destination = self.sale_id.partner_id.display_name
            contact_ref = self.sale_id.client_order_ref or ' '
            if self.sale_id.analytic_account_id:
                contact_ref += ' / ' + self.sale_id.analytic_account_id.display_name
            self.contract_ref = contact_ref
            self.laycan_to = self.sale_id.laycan_to
            self.laycan_from = self.sale_id.laycan_from
            self.picking_ids = self.sale_id.picking_ids.ids
            self.nomination_lines = [(0, 0, {'product_id': line.product_id, 'qty': line.product_uom_qty,
                                             'qty_done': line.product_uom_qty, 'product_packaging_id':
                                                 line.product_packaging_id.id, 'product_packaging_qty':
                                                 line.product_packaging_qty}
                                      ) for line in self.sale_id.order_line]
            self.account_analytic_id = self.sale_id.analytic_account_id or False

    name = fields.Char(
        copy=False, compute='_compute_name', readonly=False, store=True,
        index=True, tracking=True)
    type = fields.Selection(selection=[('sale', 'Sale'), ('purchase', 'Purchase'), ('sale_trucks', 'Sale Trucks'),
                                       ('purchase_trucks', 'Purchase  Trucks'), ('sale_vessels', 'Sale Vessels'),
                                       ('purchase_vessels', 'Purchase Vessels'), ], required=True, store=True,
                            index=True, readonly=True, tracking=True, default="sale", change_default=True)
    nomination_type_id = fields.Many2one('bio.nomination.type')
    partner_id = fields.Many2one('res.partner')
    sale_id = fields.Many2one('sale.order', string='Sale Order', domain="[('partner_id', '=', partner_id)]")
    purchase_id = fields.Many2one('purchase.order', string='Purchase Order')
    company_id = fields.Many2one(
        'res.company', default=lambda self: self.env.company)
    logo = fields.Binary(related='company_id.logo')
    sale_ids = fields.Many2many('sale.order', string='Sales Orders')
    picking_ids = fields.Many2many('stock.picking', string='Stock Picking')
    user_id = fields.Many2one('res.users', copy=False, tracking=True,
                              string='Salesperson',
                              default=lambda self: self.env.user)
    freight_charges = fields.Many2one('account.incoterms', copy=False)
    vat = fields.Char(string="Our Vat Number", default=lambda self: self.env.company.vat)
    contract_ref = fields.Char()
    previous_cargo = fields.Text()
    transport_arranger = fields.Many2one('bio.nomination.code', string="Code of transport arranger")
    laycan_from = fields.Date()
    laycan_to = fields.Date()
    surveyor_id = fields.Many2one('res.partner', domain="[('inspector', '=', True)]",
                                  context="{'default_inspector':True}")
    surveyor_code = fields.Text("Surveyor Instructions")
    surveyor_product_ids = fields.Many2many("product.product", 'surveyor_product_rel',
                                            domain="[('detailed_type', '!=', 'product')]", string='Surveyor Code')

    # origin_country_id = fields.Many2one('res.country', 'Origin Country')
    # origin_state_id = fields.Many2one('res.country.state')
    demurrage_rate = fields.Float()
    currency_id = fields.Many2one('res.currency')
    loading_terms = fields.Many2many('bio.nomination.term')
    pickup_place = fields.Char()
    pickup_date_from = fields.Date()
    pickup_date_to = fields.Date()
    delivery_date_from = fields.Date()
    delivery_date_to = fields.Date()
    destination = fields.Char()
    origin = fields.Char()
    origin_state = fields.Char()
    # container info
    container_reference = fields.Char()
    container_pin_code = fields.Char()
    container_returns_date_from = fields.Date()
    container_returns_date_to = fields.Date()
    # vessel info
    vessel_id = fields.Many2one('bio.vessel', string="Vessel Name")
    vessel_num = fields.Char(related='vessel_id.description', string="Vessel No Reg")
    vessel_owner_id = fields.Many2one(related='vessel_id.partner_id', string="Vessel Owner")
    documents_provide = fields.Selection([('cp', 'Connossement + packinglist'), ('bc', 'BL + COO'),
                                          ('bcec', 'BL + COO + EAD + COQ'), ('si', 'See instructions')],)
    attachment_ids = fields.Many2many('ir.attachment', string="Documents")
    comments = fields.Text()
    transporter_id = fields.Many2one(
        'res.partner', domain=lambda self: [('transporter', '=', True)])
    receiver_id = fields.Many2one(
        'res.partner')
    # adress receiver
    street = fields.Char(related='receiver_id.street')
    street2 = fields.Char(related='receiver_id.street2')
    zip = fields.Char(related='receiver_id.zip')
    city = fields.Char(related='receiver_id.city')
    state_id = fields.Many2one(related='receiver_id.state_id')
    country_id = fields.Many2one(related='receiver_id.country_id')
    receiver_vat = fields.Char(related='receiver_id.vat', string="TVA")
    agent_id = fields.Many2one(
        comodel_name='res.partner', domain=lambda self: [('agent', '=', True)],
        string="Agent")
    agent_email = fields.Char(related='agent_id.email')
    agent_phone = fields.Char(related='agent_id.phone')

    # palettes info
    palettes_type = fields.Many2one('product.product')
    palettes_qty = fields.Integer()
    caution = fields.Float(related='palettes_type.lst_price')
    email_from = fields.Many2one('res.users', copy=False, tracking=True, string='From',
                                 default=lambda self: self.env.user)
    recipient_ids = fields.Many2many('res.partner', 'res_partner_recipient_rel', string='To')
    attn_ids = fields.Many2many('res.partner', 'res_partner_attn_rel', string='Attn')
    email_cc = fields.Char('Cc', help="Carbon copy recipients (placeholders may be used here)",
                           default=lambda self: self.env.company.email)

    phone = fields.Char(related='email_from.phone', string='Direct phone.')
    seq_reference = fields.Integer(compute='_compute_seq_reference', store=True)
    seq_reference_so = fields.Integer(compute='_compute_seq_reference', store=True)
    reference = fields.Char(compute='_compute_seq_reference', store=True)
    cost_ids = fields.One2many('bio.nomination.cost', 'nomination_id',
                               default=lambda self:
                               [(0, 0, {'name': c.id}) for c in self.env['bio.nomination.cost.type'].search([])],
                               string="Costs")
    account_analytic_id = fields.Many2one('account.analytic.account', required=1)
    nomination_lines = fields.One2many('bio.nomination.line', 'nomination_id')

    @api.depends('purchase_id', 'sale_id')
    def _compute_seq_reference(self):
        for record in self:
            record.reference = False
            record.seq_reference = False
            record.seq_reference_so = False
            if record.purchase_id and not record.seq_reference and record.type in ['purchase_vessels',
                                                                                   'purchase_trucks']:
                self.env.cr.execute("""SELECT  max(seq_reference) FROM bio_nomination WHERE purchase_id = %s""",
                                    (record.purchase_id.id,))
                max = self.env.cr.fetchone()[0]
                record.seq_reference = max and max + 1 or 1
                record.reference = '%s - %s' % (
                    record.purchase_id.name, record.seq_reference and str(record.seq_reference).rjust(3, '0') or '000')

            elif record.sale_id and not record.seq_reference_so and record.type in ['sale_vessels', 'sale_trucks']:
                self.env.cr.execute("""SELECT  max(seq_reference_so) FROM bio_nomination WHERE sale_id = %s""",
                                    (record.sale_id.id,))
                max = self.env.cr.fetchone()[0]
                record.seq_reference_so = max and max + 1 or 1
                record.reference = '%s - %s' % (
                    record.sale_id.name, record.seq_reference_so and str(
                        record.seq_reference_so).rjust(3, '0') or '000')

    @api.depends('reference', 'type', 'container_reference', 'vessel_id')
    def _compute_name(self):
        for record in self:
            name = record.reference or ''
            if record.type in ('sale_trucks', 'purchase_trucks'):
                name += '- %s' % record.container_reference
            else:
                if record.vessel_id:
                    name += '- %s' % record.vessel_id.name
            record.name = name

    @api.onchange('type', 'partner_id')
    def _onchange_partner(self):
        if self.partner_id:
            self.recipient_ids = [(6, 0, [self.partner_id.id])] or False
            self.attn_ids = self.partner_id.child_ids and [(6, 0, self.partner_id.child_ids.ids)] or False
        if self.type in ('sale_trucks', 'purchase_trucks'):
            self.nomination_type_id = self.env.ref(
                'bio_nomination.bio_nomination_trucks').id
        if self.type in ('sale_vessels', 'purchase_vessels'):
            self.nomination_type_id = self.env.ref(
                'bio_nomination.bio_nomination_vessels').id
        if self.type in ('purchase_trucks', 'purchase_vessels'):
            return {'domain': {'purchase_id': [('partner_id', '=', self.partner_id.id)],
                               'partner_id': [('supplier_rank', '>=', 1)]}}
        if self.type in ('sale_trucks', 'sale_vessels'):
            return {'domain': {'partner_id': [('customer_rank', '>=', 1)]}}

    def action_nomination_sent(self):
        self.ensure_one()
        template = self.env.ref(
            'bio_nomination.email_template_bio_nomination',
            raise_if_not_found=False)
        lang = False
        if template:
            lang = template._render_lang(self.ids)[self.id]
        if not lang:
            lang = get_lang(self.env).code
        compose_form = self.env.ref(
            'bio_nomination.bio_nomination_send_wizard_form',
            raise_if_not_found=False)
        ctx = dict(
            default_model='bio.nomination',
            default_res_id=self.id,
            default_res_model='bio.nomination',
            default_use_template=bool(template),
            default_partner_ids=self.recipient_ids.ids,
            default_template_id=template and template.id or False,
            default_composition_mode='comment',
            model_description=self.with_context(lang=lang)._name,
            force_email=True,
        )
        return {
            'name': _('Send Nomination'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'bio.nomination.send',
            'views': [(compose_form.id, 'form')],
            'view_id': compose_form.id,
            'target': 'new',
            'context': ctx,
        }
