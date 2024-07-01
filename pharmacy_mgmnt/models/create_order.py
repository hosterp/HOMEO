from openerp import api, models, fields
from openerp.osv import osv
from datetime import datetime, timedelta


class CreateOrder(models.Model):
    _name = "create.order"
    _description = 'Create Order'
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
    stock_view_ids = fields.One2many("stock.create.order.lines", "stock_view_line_id")
    order_ids = fields.One2many("create.order.lines", "stock_order_line_id")
    sales_order_ids = fields.One2many("sales.order.lines", "sales_order_line_id")
    purchase_order_ids = fields.One2many("stock.purchase.order.lines", "purchase_order_line_id")
    date_field = fields.Date(string='Date', default=fields.Date.today)
    state = fields.Selection([('draft', 'Draft'), ('order', 'Order'), ('purchased', 'Purchased')]
                             , required=True, default='draft')
    @api.multi
    def order_purchased(self):
        if self.state == "order":
            self.state = "purchased"

    @api.multi
    def print_stock_order_report_excel(self):
        datas = {
            'ids': self._ids,
            'model': self._name,
            'form': self.read(),
            'context': self._context,
        }
        if self.state == "draft":
            self.state = "order"
        return {'type': 'ir.actions.report.xml',
                'report_name': 'pharmacy_mgmnt.print_create_order_report_xlsx.xlsx',
                'datas': datas
                }

    @api.multi
    def print_stock_order_report(self):
        if self.stock_view_ids:
            new_lines = []
            for rec in self.stock_view_ids:
                if rec.number_of_order != 0:
                    new_lines.append((0, 0, {

                        'medicine_id': rec.medicine_id.id,
                        'rack': rec.rack.id,
                        'potency': rec.potency.id,
                        # 'company': rec.company.id,
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
            [('model', '=', 'create.order'), ('report_name', '=', 'pharmacy_mgmnt.report_create_order_template',)])
        data.download_filename = 'Order Report.pdf'
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'pharmacy_mgmnt.report_create_order_template',
            'file': 'filename',
            'datas': datas,
            'report_type': 'qweb-pdf',
        }

    @api.model
    def create(self, vals):
        if vals.get('sl_no', 'New') == 'New':
            vals['sl_no'] = self.env['ir.sequence'].next_by_code(
                'create.order') or 'New'
        result = super(CreateOrder, self).create(vals)
        return result

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
                        'company': rec.company.id,
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
    def stock_load(self):
        for rec in self:
            # Clear existing stock view lines if present
            if rec.stock_view_ids:
                rec.stock_view_ids = [(5, 0, 0)]

            # Prepare domain filter based on UI inputs
            domain = []
            if rec.name:
                domain += [('supplier_id', '=', rec.name.id)]
            if rec.med_category:
                domain += [('medicine_1.made_in', '=', rec.med_category)]
            if rec.group_id:
                domain += [('medicine_grp1', '=', rec.group_id.id)]
            if rec.potency_id:
                domain += [('potency', '=', rec.potency_id.id)]
            if rec.packing_id:
                domain += [('medicine_name_packing', '=', rec.packing_id.id)]
            if rec.company_id:
                domain += [('company', '=', rec.company_id.id)]
            if rec.medicine_id:
                domain += [('medicine_1', '=', rec.medicine_id.id)]
            if rec.date_from:
                domain += [('stock_date', '>=', rec.date_from)]
            if rec.date_to:
                domain += [('stock_date', '<=', rec.date_to)]

            # Search for stock items based on domain
            stock_items = self.env['entry.stock'].search(domain)

            # Prepare list to store stock view lines
            stock_view_lines = []

            for line in stock_items:
                ex_qty = 0
                sale_qty = 0

                # Calculate expired quantity if applicable
                if line.expiry_date and line.expiry_date <= fields.Date.today():
                    ex_qty += line.quantity

                # Calculate sales quantity for the batch
                if line.batch:
                    sale_domain = [
                        ('invoice_id.type', '=', 'out_invoice'),
                        ('invoice_id.state', 'in', ['paid', 'open']),
                        ('batch', '=', line.batch)
                    ]
                    if rec.date_from:
                        sale_domain += [('create_date', '>=', rec.date_from)]
                    if rec.date_to:
                        sale_domain += [('create_date', '<=', rec.date_to)]

                    sales_orders = self.env['account.invoice.line'].search(sale_domain)
                    for qty in sales_orders:
                        sale_qty += qty.quantity

                stock_view_lines.append((0, 0, {
                    'medicine_id': line.medicine_1.id,
                    'rack': line.rack.id,
                    'company': line.company.id,
                    'potency': line.potency.id,
                    'medicine_name_packing': line.medicine_name_packing.id,
                    'medicine_grp1': line.medicine_grp1.id,
                    'qty': line.qty,
                    'ex_qty': ex_qty,
                    'sale_qty': sale_qty,
                    'mrp': line.mrp,
                    'batch': line.batch,
                    'manf_date': line.manf_date,
                    'expiry_date': line.expiry_date,
                }))

            rec.stock_view_ids = stock_view_lines


class StockOrderLine(models.Model):
    _name = "create.order.lines"
    _description = 'Stock Order Line'

    stock_order_line_id = fields.Many2one("create.order", string="Medicine Entry")
    new_order = fields.Integer(string="New Order")

    medicine_id = fields.Many2one('product.product', string="Medicine")
    rack = fields.Many2one('product.medicine.types', string="rack")
    company = fields.Many2one('product.medicine.responsible', string="company")
    potency = fields.Many2one('product.medicine.subcat', string="potency")
    medicine_name_packing = fields.Many2one('product.medicine.packing', string="medicine_name_packing")
    medicine_grp1 = fields.Many2one('product.medicine.group', string="medicine_grp1")
    qty = fields.Integer(string="qty")
    mrp = fields.Float(string="mrp")
    batch_2 = fields.Many2one('med.batch', string="batch_2")
    batch = fields.Char( string="Batch")
    manf_date = fields.Date()
    expiry_date = fields.Date()

class StockCreateOrderLine(models.Model):
    _name = "stock.create.order.lines"
    _description = 'Stock View Line'

    stock_view_line_id = fields.Many2one("create.order", string="Medicine Entry")
    number_of_order = fields.Integer("New Order")
    get_purchase = fields.Boolean(default=False, string="Purchase Details")
    expiry_alert_date = fields.Date(compute='_compute_expiry_alert_date', string='Expiry Alert Date', store=True)
    ex_qty = fields.Integer(string="Expired Qty")
    sale_qty = fields.Integer(string="Sale Qty")

    medicine_id = fields.Many2one('product.product', string="Medicine")
    rack = fields.Many2one('product.medicine.types', string="rack")
    company = fields.Many2one('product.medicine.responsible', string="company")
    potency = fields.Many2one('product.medicine.subcat', string="potency")
    medicine_name_packing = fields.Many2one('product.medicine.packing', string="medicine_name_packing")
    medicine_grp1 = fields.Many2one('product.medicine.group', string="medicine_grp1")
    qty = fields.Integer(string="qty")
    mrp = fields.Float(string="mrp")
    batch_2 = fields.Many2one('med.batch', string="batch_2")
    batch = fields.Char( string="Batch")
    manf_date = fields.Date()
    expiry_date = fields.Date()

    @api.depends('expiry_date')
    def _compute_expiry_alert_date(self):
        for record in self:
            if record.expiry_date:
                expiry_date = datetime.strptime(record.expiry_date, '%Y-%m-%d').date()
                record.expiry_alert_date = expiry_date - timedelta(days=180)
            else:
                record.expiry_alert_date = False