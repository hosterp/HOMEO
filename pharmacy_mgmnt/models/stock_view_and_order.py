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
    stock_view_ids = fields.One2many("stock.view.order.lines", "stock_view_line_id")
    order_ids = fields.One2many("stock.order.lines", "stock_order_line_id")
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
            print(vals, 'valsssssssssssssssssssssssssss')
        result = super(StockViewOrder, self).create(vals)
        return result

    @api.multi
    def order_purchased(self):
        if self.state == "order":
            self.state = "purchased"

    @api.multi
    def create_order_button(self):
        if self.stock_view_ids:
            new_lines = []
            for rec in self.stock_view_ids:
                if rec.number_of_order != 0:
                    new_lines.append((0, 0, {
                        # 'medicine_1': rec.medicine_1.id,
                        'medicine_id': rec.medicine_id.id,
                        'rack': rec.rack.id,
                        'potency': rec.potency.id,
                        'medicine_name_packing': rec.medicine_name_packing.id,
                        'medicine_grp1': rec.medicine_grp1.id,
                        'qty': rec.qty,
                        'mrp': rec.mrp,
                        'batch_2': rec.batch_2,
                        'manf_date': rec.manf_date,
                        'expiry_date': rec.expiry_date,
                        'new_order': rec.number_of_order,
                    }))
                    # self.write({'order_ids': new_lines})
                    rec.number_of_order = 0
            self.order_ids = new_lines

    @api.multi
    def print_stock_order_report(self):
        if self.stock_view_ids:
            new_lines = []
            for rec in self.stock_view_ids:
                if rec.number_of_order != 0:
                    new_lines.append((0, 0, {
                        'medicine_1': rec.medicine_1.id,
                        'medicine_id': rec.medicine_id.id,
                        'rack': rec.rack.id,
                        'potency': rec.potency.id,
                        'medicine_name_packing': rec.medicine_name_packing.id,
                        'medicine_grp1': rec.medicine_grp1.id,
                        'qty': rec.qty,
                        'mrp': rec.mrp,
                        'batch_2': rec.batch_2,
                        'manf_date': rec.manf_date,
                        'expiry_date': rec.expiry_date,
                        'new_order': rec.number_of_order,
                    }))
                    # self.write({'order_ids': new_lines})
                    rec.number_of_order = 0
            self.order_ids = new_lines
        if self.state == "draft":
            self.state = "order"
        datas = {
            'ids': self._ids,
            'model': self._name,
            'form': self.read(),
            'context': self._context,
        }
        data = self.env['ir.actions.report.xml'].search(
            [('model', '=', 'stock.view.order'), ('report_name', '=', 'pharmacy_mgmnt.report_stock_order_template',)])
        data.download_filename = 'Stock order report.pdf'
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'pharmacy_mgmnt.report_stock_order_template',
            'file': 'filename',
            'datas': datas,
            'report_type': 'qweb-pdf',
        }

    @api.multi
    def stock_load(self):
        if self.stock_view_ids:
            new_lines = []
            for rec in self.stock_view_ids:
                if rec.number_of_order != 0:
                    new_lines.append((0, 0, {
                        'medicine_1': rec.medicine_1.id,
                        'medicine_id': rec.medicine_id.id,
                        'rack': rec.rack.id,
                        'potency': rec.potency.id,
                        'medicine_name_packing': rec.medicine_name_packing.id,
                        'medicine_grp1': rec.medicine_grp1.id,
                        'qty': rec.qty,
                        'mrp': rec.mrp,
                        'batch_2': rec.batch_2,
                        'manf_date': rec.manf_date,
                        'expiry_date': rec.expiry_date,
                        'new_order': rec.number_of_order,
                    }))
                    # self.write({'order_ids': new_lines})
            self.order_ids = new_lines

        domain = []
        if self.name:
            domain += [('supplier_id', '=', self.name.id)]
        if self.med_category:
            domain += [('medicine_1.made_in', '=', self.med_category)]
        if self.group_id:
            domain += [('medicine_grp1', '=', self.group_id.id)]
        if self.potency_id:
            domain += [('potency', '=', self.potency_id.id)]
        if self.packing_id:
            domain += [('medicine_name_packing', '=', self.packing_id.id)]
        if self.company_id:
            domain += [('company', '=', self.company_id.id)]
        if self.medicine_id:
            domain += [('medicine_1', '=', self.medicine_id.id)]
        if self.date_from:
            domain += [('stock_date', '>=', self.date_from)]
        if self.date_to:
            domain += [('stock_date', '<=', self.date_to)]
        for rec in self:
            if rec.stock_view_ids:
                rec.stock_view_ids = [(5, 0, 0)]

            list = []
            stock_items = self.env['entry.stock'].search(domain)

            if stock_items:
                for line in stock_items:
                    found_duplicate = False

                    for item in list:
                        if (
                                line.medicine_1.id == item[2]['medicine_id'] and
                                line.potency.id == item[2]['potency'] and
                                line.medicine_name_packing.id == item[2]['medicine_name_packing'] and
                                line.medicine_grp1.id == item[2]['medicine_grp1'] and
                                line.company.id == item[2]['company']
                        ):
                            item[2]['qty'] += line.qty
                            found_duplicate = True
                            if line.expiry_date <= fields.Date.today():
                                item[2]['ex_qty'] += line.qty
                            break

                    if not found_duplicate:
                        if line.expiry_date <= fields.Date.today():
                            ex_qty = line.qty
                        else:
                            ex_qty = 0
                        list.append([0, 0, {
                            'medicine_id': line.medicine_1.id,
                            'rack': line.rack.id,
                            'company': line.company.id,
                            'potency': line.potency.id,
                            'medicine_name_packing': line.medicine_name_packing.id,
                            'medicine_grp1': line.medicine_grp1.id,
                            'qty': line.qty,
                            'ex_qty': ex_qty,
                            'mrp': line.mrp,
                            'batch_2': line.batch_2,
                            'manf_date': line.manf_date,
                            'expiry_date': line.expiry_date,
                        }])

            rec.stock_view_ids = list
            domain = []

            # for rec in self:
        #     if rec.stock_view_ids:
        #         rec.stock_view_ids = [(5, 0, 0)]
            # rec.account_id = 25
            # rec.stock_view_ids = []
            list = []
            # stock_items = self.env['entry.stock'].search(domain)
            # if stock_items:
            #     for line in stock_items:
            #             list.append([0, 0, {
            #                 'medicine_id': line.medicine_1.id,
            #                 'rack': line.rack.id,
            #                 'potency': line.potency.id,
            #                 'medicine_name_packing': line.medicine_name_packing.id,
            #                 # 'company': line.company.id,
            #                 'medicine_grp1': line.medicine_grp1.id,
            #                 'qty': line.qty,
            #                 'mrp': line.mrp,
            #                 'batch_2': line.batch_2,
            #                 'manf_date': line.manf_date,
            #                 'expiry_date': line.expiry_date,
            #             }])
            # rec.stock_view_ids = list
            # domain = []

    @api.multi
    def get_purchase(self):
        domain = []
        for rec in self.stock_view_ids:
            if rec.get_purchase == True:
                domain = [('invoice_id.type', '=', 'in_invoice'),('invoice_id.state', '=', 'paid')]
                if rec.medicine_id.id:
                    domain += [('product_id', '=', rec.medicine_id.id)]
                if rec.potency.id:
                    domain += [('medicine_name_subcat', '=', rec.potency.id)]
                if rec.company.id:
                    domain += [('product_of', '=', rec.company.id)]
                if rec.medicine_grp1.id:
                    domain += [('medicine_grp', '=', rec.medicine_grp1.id)]
                if self.date_from:
                    domain += [('invoice_id.date_invoice', '>=', self.date_to)]
                if self.date_to:
                    domain += [('invoice_id.date_invoice', '<=', self.date_from)]
                if self.name:
                    domain += [('invoice_id.partner_id', '<=', self.name.id)]
        for rec in self:
            if rec.purchase_order_ids:
                rec.purchase_order_ids = [(5, 0, 0)]
            # rec.account_id = 25
            # rec.sales_order_ids = []
            list = []
            invoices = self.env['account.invoice.line'].search(domain)
            if invoices:
                for line in invoices:
                    if line.invoice_id.state == 'paid':
                        list.append([0, 0, {
                            'invoice_id':line.invoice_id.id,
                            'partner_id': line.invoice_id.partner_id.id,
                            'date_invoice': line.invoice_id.date_invoice,
                            'quantity': line.quantity,
                            'product_id': line.product_id.id,
                            'product_of': line.product_of.id,
                            'medicine_grp': line.medicine_grp.id,
                            'medicine_name_subcat': line.medicine_name_subcat.id,
                            'batch_2':line.batch_2
                        }
                                     ])
            rec.purchase_order_ids = list
            domain = []
        for rec in self.stock_view_ids:
            if rec.get_purchase == True:
                rec.get_purchase = False

    @api.multi
    def get_sales(self):
        domain = []
        for rec in self.purchase_order_ids:
            if rec.get_sales == True:
                domain = [('invoice_id.type', '=', 'out_invoice'),('invoice_id.state', '=', 'paid')]
                if rec.product_id.id:
                    domain += [('product_id', '=', rec.product_id.id)]
                if rec.medicine_name_subcat.id:
                    domain += [('medicine_name_subcat', '=', rec.medicine_name_subcat.id)]
                if rec.product_of.id:
                    domain += [('product_of', '=', rec.product_of.id)]
                if rec.medicine_grp.id:
                    domain += [('medicine_grp', '=', rec.medicine_grp.id)]
                if rec.batch_2.id:
                    domain += [('medicine_grp', '=', rec.batch_2.id)]
                if self.date_from:
                    domain += [('invoice_id.date_invoice', '>=', self.date_to)]
                if self.date_to:
                    domain += [('invoice_id.date_invoice', '<=', self.date_from)]
        for rec in self:
            if rec.sales_order_ids:
                rec.sales_order_ids = [(5, 0, 0)]
            # rec.account_id = 25
            # rec.sales_order_ids = []
            list = []
            invoices = self.env['account.invoice.line'].search(domain)
            if invoices:
                for line in invoices:
                    if line.invoice_id.state == 'paid':
                        list.append([0, 0, {
                            'invoice_id': line.invoice_id.id,
                            'partner_id': line.invoice_id.partner_id.id,
                            'date_invoice': line.invoice_id.date_invoice,
                            'quantity': line.quantity,
                            'product_id': line.product_id.id,
                            'product_of': line.product_of.id,
                            'medicine_grp': line.medicine_grp.id,
                            'medicine_name_subcat': line.medicine_name_subcat.id,
                        }
                                     ])
            rec.sales_order_ids = list
            domain = []
        for rec in self.purchase_order_ids:
            if rec.get_sales == True:
                rec.get_sales = False


class StockViewOrderLine(models.Model):
    _name = "stock.view.order.lines"
    _description = 'Stock View Line'
    # _inherits = {'entry.stock': 'medicine_1'}

    stock_view_line_id = fields.Many2one("stock.view.order", string="Medicine Entry")
    # medicine_1 = fields.Many2one('entry.stock')
    number_of_order = fields.Integer("New Order")
    # get_sales = fields.Boolean(default=False, string="Sales Details")
    get_purchase = fields.Boolean(default=False, string="Purchase Details")
    expiry_alert_date = fields.Date(compute='_compute_expiry_alert_date', string='Expiry Alert Date', store=True)
    ex_qty = fields.Integer(string="Expired Qty")


    medicine_id = fields.Many2one('product.product', string="Medicine")
    rack = fields.Many2one('product.medicine.types', string="rack")
    company = fields.Many2one('product.medicine.responsible', string="company")
    potency = fields.Many2one('product.medicine.subcat', string="potency")
    medicine_name_packing = fields.Many2one('product.medicine.packing', string="medicine_name_packing")
    medicine_grp1 = fields.Many2one('product.medicine.group', string="medicine_grp1")
    qty = fields.Integer(string="qty")
    mrp = fields.Float(string="mrp")
    batch_2 = fields.Many2one('med.batch', string="batch_2")
    manf_date = fields.Date()
    expiry_date = fields.Date()

    @api.depends('expiry_date')
    def _compute_expiry_alert_date(self):
        for record in self:
            if record.expiry_date:
                expiry_date = datetime.strptime(record.expiry_date, '%Y-%m-%d').date()
                record.expiry_alert_date = expiry_date - timedelta(days=180)
                # print('hello', record.expiry_alert_date)
            else:
                record.expiry_alert_date = False


class StockOrderLine(models.Model):
    _name = "stock.order.lines"
    _description = 'Stock Order Line'
    _inherits = {'entry.stock': 'medicine_1'}

    stock_order_line_id = fields.Many2one("stock.view.order", string="Medicine Entry")
    medicine_1 = fields.Many2one('entry.stock')
    medicine_id = fields.Many2one('product.product', string="Medicine")
    new_order = fields.Integer(string="New Order")





class SalesOrderLine(models.Model):
    _name = "sales.order.lines"
    _description = 'Sales Order Line'

    sales_order_line_id = fields.Many2one("stock.view.order", string="Medicine Entry")
    invoice_id = fields.Many2one("account.invoice", "Invoice",domain=[('type','=','out_invoice')])
    partner_id = fields.Many2one("res.partner", "Customer")
    date_invoice = fields.Date("Date")
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
            'type': 'ir.actions.act_url',
            'url': redirect_url,
            'target': 'self',
        }



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

    @api.multi
    def open_invoice(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        redirect_url = "%s/web#id=%d&view_type=form&model=account.invoice&menu_id=328&action=399" % (
            base_url, self.invoice_id.id)
        return {
            'type': 'ir.actions.act_url',
            'url': redirect_url,
            'target': 'self',
        }


