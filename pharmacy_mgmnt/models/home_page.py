from openerp import models, fields, api

class HomePage(models.Model):
    _name = 'home.page'


    name=fields.Char('Name')



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