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
    med_category = fields.Selection([('indian', 'Indian'), ('german', 'German')],string="Made In")
    group_id = fields.Many2one("product.medicine.group", string="Group")
    potency_id = fields.Many2one("product.medicine.subcat", string="Potency")
    packing_id = fields.Many2one("product.medicine.packing", string="Packing")
    medicine_id = fields.Many2one("product.product", string="Medicine")
    company_id = fields.Many2one("product.medicine.responsible", string="Company")
    date_from = fields.Date(string="Date From")
    date_to = fields.Date(string="Date To")
    stock_view_ids = fields.One2many("stock.view.order.lines", "stock_view_line_id")
    order_ids = fields.One2many("stock.order.lines", "stock_order_line_id")
    date_field = fields.Date(string='Date', default=fields.Date.today)
    state = fields.Selection([('draft', 'Draft'), ('order', 'Order'), ('purchased', 'Purchased')]
                             , required=True, default='draft')

    @api.model
    def create(self, vals):
        if vals.get('sl_no', 'New') == 'New':
            vals['sl_no'] = self.env['ir.sequence'].next_by_code(
                'stock.order') or 'New'
            print(vals,'valsssssssssssssssssssssssssss')
        result = super( StockViewOrder, self).create(vals)
        return result
    @api.multi
    def order_purchased(self):
        if self.state == "order":
            self.state = "purchased"
    @api.multi
    def print_stock_order_report(self):
        if self.stock_view_ids:
            new_lines = []
            for rec in self.stock_view_ids:
                if rec.number_of_order != 0:
                    # for rec in res:
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
                    # for rec in res:
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
            # rec.account_id = 25
            # rec.stock_view_ids = []
            list = []
            stock_items = self.env['entry.stock'].search(domain)
            if stock_items:
                for line in stock_items:
                    list.append([0, 0, {'medicine_1': line.id,
                                        'medicine_id': line.medicine_1.id,
                                        'rack': line.rack.id,
                                        'potency': line.potency.id,
                                        'medicine_name_packing': line.medicine_name_packing.id,
                                        # 'company': line.company.id,
                                        'medicine_grp1': line.medicine_grp1.id,
                                        'qty': line.qty,
                                        'mrp': line.mrp,
                                        'batch_2': line.batch_2,
                                        'manf_date': line.manf_date,
                                        'expiry_date': line.expiry_date,
                                        }
                                 ])
            rec.stock_view_ids = list
            domain = []

class StockViewOrderLine(models.Model):
    _name = "stock.view.order.lines"
    _description = 'Stock View Line'
    _inherits = {'entry.stock': 'medicine_1'}


    stock_view_line_id = fields.Many2one("stock.view.order", string="Medicine Entry")
    medicine_1 = fields.Many2one('entry.stock')
    medicine_id = fields.Many2one('product.product', string="Medicine")
    number_of_order = fields.Integer("New Order")

    expiry_alert_date = fields.Date(compute='_compute_expiry_alert_date', string='Expiry Alert Date', store=True)

    @api.depends('expiry_date')
    def _compute_expiry_alert_date(self):
        for record in self:
            if record.expiry_date:
                expiry_date = datetime.strptime(record.expiry_date, '%Y-%m-%d').date()
                record.expiry_alert_date = expiry_date - timedelta(days=180)
                print('hello', record.expiry_alert_date)
                # print('hi')
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




