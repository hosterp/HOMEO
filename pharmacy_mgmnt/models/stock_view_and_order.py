from openerp import api, models, fields
from openerp.osv import osv
from datetime import datetime, timedelta


class StockViewOrder(models.Model):
    _name = "stock.view.order"
    _description = 'Stock View'
    _rec_name = 'sl_no'
    _order = 'sl_no desc'

    sl_no = fields.Char(string='sl no')
    name = fields.Many2one("res.partner", string="Supplier", domain="[('supplier', '=', True)]")
    med_category = fields.Selection([('indian', 'Indian'), ('german', 'German')], string="Made In")
    group_id = fields.Many2one("product.medicine.group", string="Group")
    potency_id = fields.Many2one("product.medicine.subcat", string="Potency")
    packing_id = fields.Many2one("product.medicine.packing", string="Packing")
    medicine_id = fields.Many2one("product.product", string="Medicine")
    company_id = fields.Many2one("product.medicine.responsible", string="Company")
    date_from = fields.Date(string="Date From")
    date_to = fields.Date(string="Date To")
    # stock_view_ids = fields.One2many("stock.view.order.lines", "stock_view_line_id")
    # order_ids = fields.One2many("stock.order.lines", "stock_order_line_id")
    sales_order_ids = fields.One2many("sales.order.lines", "sales_order_line_id")
    purchase_order_ids = fields.One2many("stock.purchase.order.lines", "purchase_order_line_id")
    date_field = fields.Date(string='Date', default=fields.Date.today)
    state = fields.Selection([('draft', 'Draft'), ('order', 'Order'), ('purchased', 'Purchased')]
                             , required=True, default='draft')

    @api.model
    def create(self, vals):
        if vals.get('sl_no', 'New') == 'New':
            vals['sl_no'] = self.env['ir.sequence'].next_by_code(
                'stock.order') or 'New'
        result = super(StockViewOrder, self).create(vals)
        return result

    @api.multi
    def order_purchased(self):
        if self.state == "order":
            self.state = "purchased"

    @api.multi
    def get_purchase(self):
        for rec in self:
            domain = [('invoice_id.type', '=', 'in_invoice'), ('invoice_id.state', 'in', ['paid', 'open'])]

            if rec.medicine_id:
                domain += [('product_id', '=', rec.medicine_id.id)]
            if rec.potency_id:
                domain += [('medicine_name_subcat', '=', rec.potency_id.id)]
            if rec.company_id:
                domain += [('product_of', '=', rec.company_id.id)]
            if rec.packing_id:
                domain += [('medicine_name_packing', '=', rec.packing_id.id)]
            if rec.group_id:
                domain += [('medicine_grp', '=', rec.group_id.id)]
            if rec.date_from:
                domain += [('invoice_id.date_invoice', '>=', rec.date_from)]
            if rec.date_to:
                domain += [('invoice_id.date_invoice', '<=', rec.date_to)]
            if rec.name:
                domain += [('invoice_id.partner_id', '=', rec.name.id)]

            if rec.purchase_order_ids:
                rec.purchase_order_ids = [(5, 0, 0)]

            purchase_order_list = []
            invoices = self.env['account.invoice.line'].search(domain)

            if invoices:
                for line in invoices:
                    if line.invoice_id.state in ['paid', 'open']:
                        purchase_order_list.append([0, 0, {
                            'invoice_id': line.invoice_id.id,
                            'partner_id': line.invoice_id.partner_id.id,
                            'date_invoice': line.invoice_id.date_invoice,
                            'quantity': line.quantity,
                            'product_id': line.product_id.id,
                            'product_of': line.product_of.id,
                            'medicine_grp': line.medicine_grp.id,
                            'medicine_name_subcat': line.medicine_name_subcat.id,
                            'batch': line.batch
                        }])

            rec.purchase_order_ids = purchase_order_list

        self.get_sales()

    @api.multi
    def get_sales(self):
        for rec in self:
            domain = [('invoice_id.type', '=', 'out_invoice'), ('invoice_id.state', 'in', ['paid', 'open'])]

            if self.sales_order_ids:
                self.sales_order_ids = [(5, 0, 0)]

            list_of_sales_orders = []

            for purchase_order in rec.purchase_order_ids:
                order_domain = list(domain)  # Create a copy of domain for each purchase order
                if purchase_order.product_id:
                    order_domain += [('product_id', '=', purchase_order.product_id.id)]
                if purchase_order.medicine_name_subcat:
                    order_domain += [('medicine_name_subcat', '=', purchase_order.medicine_name_subcat.id)]
                if purchase_order.product_of:
                    order_domain += [('product_of', '=', purchase_order.product_of.id)]
                if purchase_order.medicine_grp:
                    order_domain += [('medicine_grp', '=', purchase_order.medicine_grp.id)]
                if purchase_order.batch:
                    order_domain += [('batch', '=', purchase_order.batch)]
                if rec.date_from:
                    order_domain += [('invoice_id.date_invoice', '>=', rec.date_to)]
                if rec.date_to:
                    order_domain += [('invoice_id.date_invoice', '<=', rec.date_from)]

                sales_orders = self.env['account.invoice.line'].search(order_domain)

                if sales_orders:
                    for line in sales_orders:
                        if line.invoice_id.state in ['paid', 'open']:
                            list_of_sales_orders.append((0, 0, {
                                'invoice_id': line.invoice_id.id,
                                'partner_id': line.invoice_id.partner_id.id,
                                'date_invoice': line.invoice_id.date_invoice,
                                'quantity': line.quantity,
                                'product_id': line.product_id.id,
                                'batch': line.batch,
                                'product_of': line.product_of.id,
                                'medicine_grp': line.medicine_grp.id,
                                'medicine_name_subcat': line.medicine_name_subcat.id,
                            }))

            rec.sales_order_ids = list_of_sales_orders


class StockPurchaseOrderLine(models.Model):
    _name = "stock.purchase.order.lines"
    _description = 'Stock purchase Order Line'

    purchase_order_line_id = fields.Many2one("stock.view.order", string="Medicine Entry")
    get_sales = fields.Boolean(default=False, string="Sales Details")
    invoice_id = fields.Many2one("account.invoice", "Invoice", domain=[('type', '=', 'in_invoice')])

    partner_id = fields.Many2one("res.partner", "Supplier")
    date_invoice = fields.Date("Date")
    quantity = fields.Integer("quantity")
    product_id = fields.Many2one("product.product")
    product_of = fields.Many2one("product.medicine.responsible")
    medicine_grp = fields.Many2one("product.medicine.group")
    medicine_name_subcat = fields.Many2one("product.medicine.subcat")
    batch_2 = fields.Many2one('med.batch','Batch')
    batch = fields.Char('Batch')


    @api.multi
    def open_invoice(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        redirect_url = "%s/web#id=%d&view_type=form&model=account.invoice&menu_id=328&action=399" % (
            base_url, self.invoice_id.id)
        return {
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.invoice_id.id,
            'res_model': 'account.invoice',
            'view_id': self.env.ref('account.invoice_supplier_form').id,
            'type': 'ir.actions.act_window',
            'context': {'type': 'out_invoice'},
            'flags': {'action_buttons': True},
            # 'target': 'current',
            # 'clear': 1,
        }
        # return {
        #     'type': 'ir.actions.act_url',
        #     'url': redirect_url,
        #     'target': 'self',
        # }

class SalesOrderLine(models.Model):
    _name = "sales.order.lines"
    _description = 'Sales Order Line'

    sales_order_line_id = fields.Many2one("stock.view.order", string="Medicine Entry")
    invoice_id = fields.Many2one("account.invoice", "Invoice", domain=[('type', '=', 'out_invoice')])
    partner_id = fields.Many2one("res.partner", "Customer")
    date_invoice = fields.Date("Date")
    batch = fields.Char('Batch')
    quantity = fields.Integer("quantity")
    product_id = fields.Many2one("product.product")
    product_of = fields.Many2one("product.medicine.responsible")
    medicine_grp = fields.Many2one("product.medicine.group")
    medicine_name_subcat = fields.Many2one("product.medicine.subcat")

    @api.multi
    def open_invoice(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        redirect_url = "%s/web#id=%d&view_type=form&model=account.invoice&menu_id=331&action=400" % (
            base_url, self.invoice_id.id)
        return {
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.invoice_id.id,
            'res_model': 'account.invoice',
            'view_id': self.env.ref('account.invoice_form').id,
            'type': 'ir.actions.act_window',
            'context': {'type': 'out_invoice'},
            'flags': {'action_buttons': True},
            # 'target': 'current',
            # 'clear': 1,
        }
        # return {
        #     'type': 'ir.actions.act_url',
        #     'url': redirect_url,
        #     'target': 'self',
        # }




