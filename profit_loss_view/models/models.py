from odoo import models, fields, api, tools


class InheritAccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    ann_acc = fields.Char("Ann accounts", compute="_get_ann_name", store=True)

    @api.depends('analytic_distribution')
    def _get_ann_name(self):
        for rec in self:
            acc_obj = self.env['account.analytic.account']
            if rec.analytic_distribution:
                name_list = [acc_obj.browse(int(i)).name + ","
                             for i in rec.analytic_distribution.keys()]
                rec.ann_acc = ", ".join([element.strip("'").rstrip(',') for element in name_list])


            else:
                rec.ann_acc = ''


class InheritSaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    ann_acc = fields.Char("Ann accounts", compute="_get_ann_name", store=True)

    @api.depends('analytic_distribution')
    def _get_ann_name(self):
        for rec in self:
            acc_obj = self.env['account.analytic.account']
            if rec.analytic_distribution:
                name_list = [acc_obj.browse(int(i)).name + ","
                             for i in rec.analytic_distribution.keys()]
                rec.ann_acc = ", ".join([element.strip("'").rstrip(',') for element in name_list])


            else:
                rec.ann_acc = ''


class InheritPurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    ann_acc = fields.Char("Ann accounts", compute="_get_ann_name", store=True)

    @api.depends('analytic_distribution')
    def _get_ann_name(self):
        for rec in self:
            acc_obj = self.env['account.analytic.account']
            if rec.analytic_distribution:
                name_list = [acc_obj.browse(int(i)).name + ","
                             for i in rec.analytic_distribution.keys()]
                rec.ann_acc = ", ".join([element.strip("'").rstrip(',') for element in name_list])


            else:
                rec.ann_acc = ''


class ProfitLossView(models.Model):
    _name = 'profit.loss.view'
    _auto = False
    _rec_name = 'name'
    _order = 'report_type DESC'

    name = fields.Char("Name")
    product_id = fields.Many2one('product.template')
    price_subtotal = fields.Monetary('Price Subtotal')
    currency_id = fields.Many2one('res.currency', string='Currency')
    description = fields.Char('Description')
    quantity = fields.Float('Quantity')
    unit_price = fields.Float('Unit Price')
    account_id = fields.Many2one('account.account', 'Account')
    analytic_account_id = fields.Char("Analytic Account")
    report_type = fields.Selection(
        [('sale_order', 'Sale Order'), ('purchase_order', 'Purchase Order'), ('expenses', 'Expenses')])

    def init(self):
        tools.drop_view_if_exists(self._cr, 'profit_loss_view')
        companies = list(tuple(self.env.companies.ids))
        companies.append(1000)
        self._cr.execute(f""" 
               CREATE OR REPLACE VIEW profit_loss_view AS
                    SELECT DISTINCT ON (id, report_type, name) id, report_type, name, product_id, price_subtotal,
                                   analytic_account_id,account_id, currency_id, description, quantity,
                                   unit_price
                    FROM 
                    ( 
                        SELECT sol.id as id,
                            sol.product_id as product_id,
                            so.name as name,
                            'sale_order' as report_type,
                            sol.price_subtotal as price_subtotal,
                            sol.ann_acc as analytic_account_id,
                            so.currency_id as currency_id,
                            NULL as account_id,
                            sol.name as description,
                            sol.product_uom_qty as quantity,
                            sol.price_unit as unit_price
                            FROM sale_order_line sol
                            LEFT JOIN sale_order so ON sol.order_id = so.id
                            WHERE so.state = 'sale' AND so.company_id in {tuple(companies)}

                        UNION
                        SELECT iol.id as id,
                            iol.product_id as product_id,
                            move.name as name,
                            'sale_order' as report_type,
                            iol.price_subtotal as price_subtotal,
                            iol.ann_acc as analytic_account_id,
                            iol.account_id as account_id,
                            move.currency_id as currency_id,
                            iol.name as description,
                            iol.quantity as quantity,
                            iol.price_unit as unit_price
                            FROM account_move_line iol
                            LEFT JOIN account_move move ON iol.move_id = move.id
                            WHERE move.state = 'posted' AND move.move_type='out_invoice'
                            AND move.invoice_origin IS NULL AND iol.display_type='product'
                            AND
                            move.company_id in {tuple(companies)}
                        
                        UNION

                        SELECT pol.id as id,
                            pol.product_id as product_id,
                            po.name as name,
                            'purchase_order' as report_type,
                            pol.price_subtotal as price_subtotal,
                            pol.ann_acc as analytic_account_id,
                            NULL as account_id,
                            po.currency_id as currency_id,
                            pol.name as description,
                            pol.product_qty as quantity,
                            pol.price_unit as unit_price
                            FROM purchase_order_line pol
                            LEFT JOIN purchase_order po ON pol.order_id = po.id
                            LEFT JOIN product_template pt on pol.product_id = pt.id
                            WHERE po.state = 'purchase' AND pt.detailed_type='product' AND
                            po.company_id in {tuple(companies)}

                        UNION 

                        SELECT bol.id as id,
                            bol.product_id as product_id,
                            move.name as name,
                            'purchase_order' as report_type,
                            bol.price_subtotal as price_subtotal,
                            bol.ann_acc as analytic_account_id,
                            bol.account_id as account_id,
                            move.currency_id as currency_id,
                            bol.name as description,
                            bol.quantity as quantity,
                            bol.price_unit as unit_price
                            FROM account_move_line bol
                            LEFT JOIN account_move move ON bol.move_id = move.id
                            LEFT JOIN product_template pt on bol.product_id = pt.id
                            WHERE move.state = 'posted' AND move.move_type='in_invoice'
                            AND move.invoice_origin IS NULL AND bol.display_type='product'
                            AND pt.detailed_type='product' AND
                            move.company_id in {tuple(companies)}

                        UNION

                        SELECT exp.id as id,
                            exp.product_id as product_id,
                            move.name as name,
                            'expenses' as report_type,
                            exp.price_subtotal as price_subtotal,
                            exp.ann_acc as analytic_account_id,
                            exp.account_id as account_id,
                            move.currency_id as currency_id,
                            exp.name as description,
                            exp.quantity as quantity,
                            exp.price_unit as unit_price
                            FROM account_move_line exp
                            LEFT JOIN account_move move ON exp.move_id = move.id
                            LEFT JOIN product_template pt on exp.product_id = pt.id
                            WHERE move.state = 'posted' AND move.move_type='in_invoice'
                            AND move.invoice_origin IS NULL AND exp.display_type='product'
                            AND pt.detailed_type='consu' AND
                            move.company_id in {tuple(companies)}
                            
                        UNION
        
                            SELECT pol.id as id,
                                pol.product_id as product_id,
                                po.name as name,
                                'expenses' as report_type,
                                pol.price_subtotal as price_subtotal,
                                pol.ann_acc as analytic_account_id,
                                NULL as account_id,
                                po.currency_id as currency_id,
                                pol.name as description,
                                pol.product_qty as quantity,
                                pol.price_unit as unit_price
                                FROM purchase_order_line pol
                                LEFT JOIN purchase_order po ON pol.order_id = po.id
                                LEFT JOIN product_template pt on pol.product_id = pt.id
                                WHERE po.state = 'purchase' AND pt.detailed_type='service' AND
                                po.company_id in {tuple(companies)}


                    ) as final_view;

               """)


class InheritAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    plv_id = fields.Many2one('profit.loss.view')
