# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################

from collections import OrderedDict
from odoo.osv import expression
from odoo import http, _
from odoo.exceptions import AccessError
from odoo.http import request
from odoo.tools import consteq
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager, get_records_pager
import base64


class CustomerPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        print(counters, 'counterscounters')
        values = super()._prepare_home_portal_values(counters)
        if 'attachment_count' in counters:
            attachment_count = request.env['ir.attachment'].sudo().search_count(
                [('res_model', '=', 'res.partner'), ('res_id', '=', request.env.user.partner_id.id)]) \
                if request.env['account.move'].check_access_rights('read', raise_exception=False) else 0
            values['attachment_count'] = attachment_count or 1
        return values

    def _get_attachment_searchbar_filters(self):
        return {
            'all': {'label': _('All'), 'domain': []},
        }

    def _get_attachment_searchbar_sortings(self):
        return {
            'date': {'label': _('Date'), 'order': 'create_date desc'},
            'name': {'label': _('Reference'), 'order': 'name desc'},
        }

    def _prepare_my_attachment_values(self, page, date_begin, date_end, sortby, filterby, domain=None,
                                      url="/my/attachments"):
        print('_prepare_my_attachment_values')
        values = self._prepare_portal_layout_values()
        print(values, 'valuesvalues')
        IrAttachment = request.env['ir.attachment'].sudo()

        # domain = expression.AND([
        #     domain or [],
        #     self._get_invoices_domain(),
        # ])
        domain = [('res_model', '=', 'res.partner'), ('res_id', '=', request.env.user.partner_id.id)]
        partner = request.env.user.partner_id

        searchbar_sortings = self._get_attachment_searchbar_sortings()
        # default sort by order
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        searchbar_filters = self._get_attachment_searchbar_filters()
        # default filter by value
        if not filterby:
            filterby = 'all'
        domain += searchbar_filters[filterby]['domain']

        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        values.update({
            'date': date_begin,
            # content according to pager and archive selected
            # lambda function to get the invoices recordset when the pager will be defined in the main method of a route
            'invoices': lambda pager_offset: IrAttachment.search(domain, order=order, limit=self._items_per_page,
                                                                 offset=pager_offset),
            'page_name': 'Attachments',
            'pager': {  # vals to define the pager.
                "url": url,
                "url_args": {'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
                "total": IrAttachment.search_count(domain),
                "page": page,
                "step": self._items_per_page,
            },
            'default_url': url,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
            'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
            'filterby': filterby,
        })
        return values

    @http.route(['/my/attachments', '/my/attachments/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_attachments(self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, **kw):
        values = self._prepare_my_attachment_values(page, date_begin, date_end, sortby, filterby)

        # pager
        pager = portal_pager(**values['pager'])

        # content according to pager and archive selected
        invoices = values['invoices'](pager['offset'])

        request.session['my_invoices_history'] = invoices.ids[:100]

        values.update({
            'invoices': invoices,
            'pager': pager,
        })
        return request.render("odoo_customer_portal.portal_my_attachments", values)

    @http.route(["/attachment/document/<int:attachment_id>/<token>"], type='http', auth='public', website=True)
    def sign_document_public(self, sign_request_id, token, **post):
        document_context = self.get_document_qweb_context(sign_request_id, token, **post)
        if not isinstance(document_context, dict):
            return document_context

        current_request_item = document_context.get('current_request_item')
        if current_request_item and current_request_item.partner_id.lang:
            http.request.env.context = dict(http.request.env.context, lang=current_request_item.partner_id.lang)
        return http.request.render('sign.doc_sign', document_context)

    @http.route(['/add/attachments', '/add/attachments/page/<int:page>'], type='http', auth="user", website=True)
    def portal_add_attachments(self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, **kw):

        return request.render("odoo_customer_portal.add_attachment_form")

    @http.route(["/attachment/uploaded"], type='http', auth='public', website=True)
    def attachment_uploaded(self, **post):
        values = {}
        partner = request.env.user.partner_id
        print(partner, 'partner', partner.name)
        if post.get('attachment', False):
            Attachments = request.env['ir.attachment']
            name = post.get('attachment').filename
            file = post.get('attachment')
            expiry_date = post.get('expiry_date')
            description = post.get('description')
            attachment = file.read()
            attachment_id = Attachments.sudo().create({
                'name': name,
                'res_name': name,
                'type': 'binary',
                'description': description,
                'expiry_date': expiry_date,
                'res_model': 'res.partner',
                'res_id': partner.id,
                'datas': base64.b64encode(attachment),
            })
            value = {
                'attachment': attachment_id
            }
            return request.redirect('/my/attachments')
            # return request.render("modulename.template_to_render", value)

    # @http.route(['/my/attachment/<int:item_id>'], type='http', auth='user', website=True)
    # def portal_my_attachment(self, item_id, **kwargs):
    #     partner_id = request.env.user.partner_id
    #     sign_item_sudo = request.env['sign.request.item'].sudo().browse(item_id)
    #     if not sign_item_sudo.exists() \
    #             or sign_item_sudo.partner_id != partner_id \
    #             or sign_item_sudo.sign_request_id.state == 'canceled' \
    #             or (sign_item_sudo.state == 'sent' and sign_item_sudo.is_mail_sent is False):
    #         return request.redirect('/my/')
    #     url = f'/sign/document/{sign_item_sudo.sign_request_id.id}/{sign_item_sudo.access_token}?portal=1'
    #     values = {
    #         'page_name': 'signature',
    #         'my_sign_item': sign_item_sudo,
    #         'url': url
    #     }
    #     values = self._get_page_view_values(sign_item_sudo, sign_item_sudo.access_token, values,
    #                                         'my_signatures_history', False, **kwargs)
    #     return request.render('sign.sign_portal_my_request', values)

    # def _prepare_portal_layout_values(self):
    #     values = super(CustomerPortal, self)._prepare_portal_layout_values()
    #     partner = request.env.user.partner_id
    #     customerRfq = request.env['customer.rfq'].sudo()
    #     rfqCount = customerRfq.search_count(['|',
    #         ('message_partner_ids', 'child_of', [partner.commercial_partner_id.id]),
    #         ('customer_ids', 'child_of', [partner.commercial_partner_id.id]),
    #         ('state', 'in', ['sent', 'cancel', 'done'])
    #     ])
    #     values.update({
    #         'rfq_count': rfqCount,
    #     })
    #     return values
    #
    # def _rfq_check_access(self, rfq_id, access_token=None):
    #     rfqObj = request.env['customer.rfq'].browse([rfq_id])
    #     rfqObjSudo = rfqObj.sudo()
    #     try:
    #         rfqObj.check_access_rights('read')
    #         rfqObj.check_access_rule('read')
    #     except AccessError:
    #         if not access_token or not consteq(rfqObjSudo.access_token, access_token):
    #             raise
    #     return rfqObjSudo
    #
    # def _rfq_get_page_view_values(self, rfqObjSudo, access_token, **kwargs):
    #     rfqHistoryModel = request.env['customer.rfqhistory'].sudo()
    #     currentLogUser = request.env.user
    #     loggedPartner = currentLogUser.partner_id
    #     customerIds = rfqObjSudo.customer_ids
    #     offerPrice = 'yes'
    #     if loggedPartner not in customerIds:
    #         offerPrice = 'no'
    #     rfqHstry = rfqHistoryModel.search([('customerrfq_id', '=', rfqObjSudo.id),
    #                                        ('name', '=', loggedPartner.id)])
    #     mpPrice, myEstDel, myNote = rfqHstry.quoted_price, rfqHstry.quoted_del_date, rfqHstry.quoted_note if rfqHstry else ''
    #     IrConfigPrmtrSudo = request.env['ir.config_parameter'].sudo()
    #     sumbitMsg = IrConfigPrmtrSudo.get_param(
    #         'odoo_customer_portal.msg_quote_submit'
    #     ) or "Thanks! We have received your quote. We will revert back to you if your quote will get approved."
    #     acceptMsg = IrConfigPrmtrSudo.get_param(
    #         'odoo_customer_portal.msg_quote_accecpt'
    #     ) or "Congratulations! we have accepted your quotation, we'll soon create the purchase order for you." \
    #          " We will look forward to a long-term business relationship with you"
    #     cancelMsg = IrConfigPrmtrSudo.get_param(
    #         'odoo_customer_portal.msg_rfq_cancel'
    #     ) or "Sorry! This RFQ has been cancelled."
    #     poMsg = IrConfigPrmtrSudo.get_param(
    #         'odoo_customer_portal.msg_po_create'
    #     ) or "Congratulations! A Purchase Order has been created for this RFQ."
    #     rejectMsg = ''
    #     if rfqObjSudo.assign_customer and rfqObjSudo.assign_customer.id != loggedPartner.id:
    #         rejectMsg = IrConfigPrmtrSudo.get_param(
    #             'odoo_customer_portal.msg_rfq_reject'
    #         ) or "We regret that your quote has not been accepted. We will be glad to give you an another opportunity soon."
    #     values = {
    #         'rfq_obj': rfqObjSudo,
    #         'my_price': mpPrice,
    #         'offer_price': offerPrice,
    #         'my_del_date': myEstDel,
    #         'my_note': myNote,
    #         'msg_submit': sumbitMsg,
    #         'msg_accept': acceptMsg,
    #         'msg_cancel': cancelMsg,
    #         'msg_reject': rejectMsg,
    #         'msg_po': poMsg,
    #         'page_name': 'rfq',
    #         'bootstrap_formatting': True,
    #         'report_type': 'html',
    #     }
    #     if access_token:
    #         values['access_token'] = access_token
    #
    #     if kwargs.get('error'):
    #         values['error'] = kwargs['error']
    #     if kwargs.get('warning'):
    #         values['warning'] = kwargs['warning']
    #     if kwargs.get('success'):
    #         values['success'] = kwargs['success']
    #
    #     history = request.session.get('my_rfqs_history', [])
    #     values.update(get_records_pager(history, rfqObjSudo))
    #
    #     return values
    #
    # @http.route(['/my/rfqrequests', '/my/rfqrequests/page/<int:page>'], type='http', auth="user", website=True)
    # def portal_my_rfqrequest(self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, **kw):
    #     values = self._prepare_portal_layout_values()
    #     partner = request.env.user.partner_id
    #     customerRfq = request.env['customer.rfq'].sudo()
    #     rfqHistoryModel = request.env['customer.rfqhistory'].sudo()
    #
    #     domain = ['|',
    #         ('message_partner_ids', 'child_of', [partner.commercial_partner_id.id]),
    #         ('customer_ids', 'child_of', [partner.commercial_partner_id.id]),
    #         ('state', 'in', ['sent', 'cancel', 'done'])
    #     ]
    #
    #     searchbar_sortings = {
    #         'createdate': {
    #             'label': _('Created Date'),
    #             'order': 'create_date desc'
    #         },
    #         'date': {
    #             'label': _('Closing Date'),
    #             'order': 'close_date desc'
    #         },
    #         'name': {
    #             'label': _('Reference'),
    #             'order': 'name'
    #         },
    #         'state': {
    #             'label': _('State'),
    #             'order': 'state desc'
    #         },
    #     }
    #
    #     # default sortby order
    #     if not sortby:
    #         sortby = 'createdate'
    #     sort_order = searchbar_sortings[sortby]['order']
    #
    #     searchbar_filters = {
    #         'all': {
    #             'label': _('All'),
    #             'domain': [('state', 'in', ['sent', 'done', 'cancel'])]
    #         },
    #         'progress': {
    #             'label': _('In Progress'),
    #             'domain': [('state', '=', 'sent')]
    #         },
    #         'cancel': {
    #             'label': _('Cancelled'),
    #             'domain': [('state', '=', 'cancel')]
    #         },
    #         'done': {
    #             'label': _('Done'),
    #             'domain': [('state', '=', 'done')]
    #         },
    #     }
    #     # default filter by value
    #     if not filterby:
    #         filterby = 'all'
    #     domain += searchbar_filters[filterby]['domain']
    #
    #     if date_begin and date_end:
    #         domain += [('create_date', '>', date_begin),
    #                    ('create_date', '<=', date_end)]
    #
    #     # count for pager
    #     rfqCount = customerRfq.search_count(domain)
    #     # make pager
    #     pager = request.website.pager(url="/my/rfqrequests",
    #                                   url_args={
    #                                       'date_begin': date_begin,
    #                                       'date_end': date_end,
    #                                       'sortby': sortby
    #                                   },
    #                                   total=rfqCount, page=page, step=self._items_per_page)
    #     # search the count to display, according to the pager data
    #     pageRfqrequest = customerRfq.search(domain, order=sort_order, limit=self._items_per_page,
    #                                       offset=pager['offset'])
    #     request.session['my_rfqs_history'] = pageRfqrequest.ids[:100]
    #     quoted = {}
    #     for rfqObj in pageRfqrequest:
    #         rfqId = rfqObj.id
    #         rfqHstry = rfqHistoryModel.search([('customerrfq_id', '=', rfqId),
    #                                            ('name', '=', partner.id)])
    #         quoted.update({rfqId: 'no'})
    #         if rfqHstry:
    #             quoted.update({rfqId: 'yes'})
    #
    #     values.update({
    #         'date': date_begin,
    #         'page_rfqrequest': pageRfqrequest.sudo(),
    #         'page_name': 'rfq',
    #         'quote': quoted,
    #         'pager': pager,
    #         'default_url': '/my/rfqrequests',
    #         'searchbar_sortings': searchbar_sortings,
    #         'sortby': sortby,
    #         'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
    #         'filterby': filterby,
    #     })
    #     return request.render("odoo_customer_portal.portal_my_page_rfq", values)
    #
    # @http.route(['/my/rfqrequests/<int:order>'], type='http', auth="user", website=True)
    # def rfq_followup(self, order=None, access_token=None, **kw):
    #     try:
    #         rfqObjSudo = self._rfq_check_access(order, access_token=access_token)
    #     except AccessError:
    #         return request.redirect('/my')
    #
    #     values = self._rfq_get_page_view_values(rfqObjSudo, access_token, **kw)
    #     return request.render("odoo_customer_portal.rfq_followup", values)
    #
    # @http.route(['/update/customerprice/'], type='json', auth="user", methods=['POST'], website=True)
    # def customer_update_price(self, rfqId, offerPrice, offerDate, offerNote, customerUserId):
    #     context, env = request.context, request.env
    #     rfqModel = env['customer.rfq']
    #     res = rfqModel.sudo().update_customer_history(int(rfqId), float(offerPrice), offerDate, offerNote, customerUserId)
    #     return {'rfqId': rfqId}
