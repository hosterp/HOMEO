from openerp import models, fields, api

class HomePage(models.Model):
    _name = 'home.page'


    name=fields.Char('Name')
    stock_count_expired = fields.Integer(string='Stock Count Expired', compute='_compute_stock_count')
    low_stock_count = fields.Integer(string='Low Stock Count', compute='_compute_stock_low_count')
    cheque_count = fields.Integer(string='Cheque Count', compute='_compute_cheque_count')
    payment_history_count = fields.Integer(string='Payment History Count', compute='_compute_payment_history_count')


    @api.depends('payment_history_count')
    def _compute_payment_history_count(self):
        stock_model = self.env['account.invoice']
        count = stock_model.search_count([('invoice_color_class', '=','True')])
        for record in self:
            record.payment_history_count = count
            print(record.payment_history_count, 'count')

    @api.depends('stock_count_expired')
    def _compute_stock_count(self):
        stock_model = self.env['entry.stock']
        count = stock_model.search_count([('expiry_date', '<=', fields.Date.today())])
        for record in self:
            record.stock_count_expired = count
            print(record.stock_count_expired,'count')

    @api.depends('low_stock_count')
    def _compute_stock_low_count(self):
        stock_model = self.env['entry.stock']
        count = stock_model.search_count([('qty','<=','50')])
        for record in self:
            record.low_stock_count = count
            print(record.low_stock_count, 'count')

    @api.depends('cheque_count')
    def _compute_cheque_count(self):
        stock_model = self.env['cheque.entry']
        count = stock_model.search_count([('deposit_date', '=', fields.Date.today())])
        for record in self:
            record.cheque_count = count
            print(record.cheque_count, 'count')

    def call_count_of_low_stock(self,cr,uid,ids,context):
        mod_obj = self.pool.get('ir.model.data')
        act_obj = self.pool.get('ir.actions.act_window')
        result = mod_obj.get_object_reference(cr, uid, 'pharmacy_mgmnt', 'action_product_search_id_count_stock')
        id = result and result[1] or False
        result = act_obj.read(cr, uid, [id], context=context)[0]
        return result

    def call_count_of_expiry_items(self,cr,uid,ids,context):
        mod_obj = self.pool.get('ir.model.data')
        act_obj = self.pool.get('ir.actions.act_window')
        result = mod_obj.get_object_reference(cr, uid, 'pharmacy_mgmnt', 'action_product_search_id_home_page')
        id = result and result[1] or False
        result = act_obj.read(cr, uid, [id], context=context)[0]
        return result

    def call_count_of_cheque_collection(self, cr, uid, ids, context):
        mod_obj = self.pool.get('ir.model.data')
        act_obj = self.pool.get('ir.actions.act_window')
        result = mod_obj.get_object_reference(cr, uid, 'pharmacy_mgmnt', 'action_count_of_check_collection')
        id = result and result[1] or False
        result = act_obj.read(cr, uid, [id], context=context)[0]
        return result

    def call_count_of_payment_history(self, cr, uid, ids, context):
        mod_obj = self.pool.get('ir.model.data')
        act_obj = self.pool.get('ir.actions.act_window')
        result = mod_obj.get_object_reference(cr, uid, 'pharmacy_mgmnt', 'action_payment_history_count')
        id = result and result[1] or False
        result = act_obj.read(cr, uid, [id], context=context)[0]
        return result