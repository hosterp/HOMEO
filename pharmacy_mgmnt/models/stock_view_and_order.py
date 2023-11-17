from openerp import api, models, fields
from openerp.osv import osv

class StockViewOrder(models.TransientModel):
    _name = "stock.view.order"
    _description = 'Stock View'

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
            domain += [('medicine_1.med_category', '=', self.med_category)]
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


class StockViewOrderLine(models.TransientModel):
    _name = "stock.view.order.lines"
    _description = 'Stock View Line'
    _inherits = {'entry.stock': 'medicine_1'}


    stock_view_line_id = fields.Many2one("stock.view.order", string="Medicine Entry")
    medicine_1 = fields.Many2one('entry.stock')
    medicine_id = fields.Many2one('product.product', string="Medicine")
    number_of_order = fields.Integer("New Order")


class StockOrderLine(models.TransientModel):
    _name = "stock.order.lines"
    _description = 'Stock Order Line'
    _inherits = {'entry.stock': 'medicine_1'}


    stock_order_line_id = fields.Many2one("stock.view.order", string="Medicine Entry")
    medicine_1 = fields.Many2one('entry.stock')
    medicine_id = fields.Many2one('product.product', string="Medicine")
    new_order = fields.Integer(string="New Order")




