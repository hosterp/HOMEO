from openerp import models, fields, api, tools, _


# ____________________________________________SUPPLIER DISCOUNTS________________________________________________________________________
class Discountss2(models.Model):
    _name = 'list.discount2'

    company = fields.Many2one('product.medicine.responsible', 'Company')
    potency = fields.Many2one('product.medicine.subcat', 'Potency', )
    # medicine_grp1 = fields.Many2one('tax.combo.new', 'Group')
    medicine_grp1 = fields.Many2one('product.medicine.group', 'Group')
    medicine_name_packing = fields.Many2one('product.medicine.packing', 'Packing', )  # discount calculation
    discount = fields.Float('Discount(%)')
    lists_id = fields.Many2one('supplier.discounts2', string='Set Discounts')
    test_list_id = fields.Many2one('supplier.discounts', string='Set Discounts')


class Discounts(models.Model):
    _name = 'list.discount'

    company = fields.Many2one('product.medicine.responsible', 'Company')
    medicine_1 = fields.Many2one('product.product', string="Medicine")
    potency = fields.Many2one('product.medicine.subcat', 'Potency', )
    # medicine_grp1 = fields.Many2one('tax.combo.new', 'Group')
    medicine_grp1 = fields.Many2one('product.medicine.group', 'Group')
    medicine_name_packing = fields.Many2one('product.medicine.packing', 'Packing', )  # discount calculation
    discount = fields.Float('Discount(%)')
    lists_id = fields.Many2one('supplier.discounts', string='Set Discounts')


class Discounts2(models.Model):
    _name = 'group.discount'

    medicine_name_subcat = fields.Many2one('product.medicine.subcat', 'Potency', )
    medicine_name_packing = fields.Many2one('product.medicine.packing', 'Packing', )
    # medicine_grp = fields.Many2one('tax.combo.new', 'Group', )
    medicine_grp = fields.Many2one('product.medicine.group', 'Group', )
    discount = fields.Float('Discount')
    expiry_months = fields.Integer('Expiry Months')
    inv_id = fields.Float("Inv.Id", compute="_get_inv_number")

    @api.multi
    def button_save(self):
        # Your save logic goes here
        return True

    @api.multi
    def save_and_create(self):
        self.button_save()
        return {
            'name': 'Group Discount',
            'view_type': 'form',
            'view_mode': 'form,tree',
            'target': 'new',
            'res_model': 'group.discount',
            'type': 'ir.actions.act_window',
            'context': {'current_id': self.id},
        }
    @api.model
    def create(self, vals):
        result = super(Discounts2, self).create(vals)
        for rec in result:
            vals = {
                'inv_id': result.env.context.get('active_id'),
                'medicine_name_subcat': rec.medicine_name_subcat.id,
                'medicine_grp': rec.medicine_grp.id,
                'discount': rec.discount,
                'expiry_months': rec.expiry_months,

            }
            self.env['group.discount.copy'].create(vals)
            print("show id...",result.env.context.get('active_id'))
        return result

    @api.one
    def _get_inv_number(self):
        self.write({'inv_id': 7})


class DiscountsCopy(models.Model):
    _name = 'group.discount.copy'

    medicine_name_subcat = fields.Many2one('product.medicine.subcat', 'Potency', )
    medicine_name_packing = fields.Many2one('product.medicine.packing', 'Packing', )
    # medicine_grp = fields.Many2one('tax.combo.new', 'Group', )
    medicine_grp = fields.Many2one('product.medicine.group', 'Group', )
    discount = fields.Float('Discount')
    expiry_months = fields.Integer('Expiry Months')
    # lists_id = fields.Many2one('set.discount', string='Set Discount')
    inv_id = fields.Float("Inv.Id")


class SupplierDiscounts1(models.Model):
    _name = 'supplier.discounts'
    _rec_name = 'supplier'

    supplier = fields.Many2one('res.partner', 'Supplier')
    lines = fields.One2many(
        comodel_name='list.discount',
        inverse_name='lists_id',
        string='Set Discounts',
        store=True,
    )
    lines2 = fields.One2many(
        comodel_name='list.discount2',
        inverse_name='test_list_id',
        string='Set Discounts',
        store=True,
    )
    
    @api.onchange('supplier')
    def supplier_onchange(self):
        for rec in self:
            if rec.supplier:
                discounts = self.env['supplier.discounts'].search([('supplier','=',rec.supplier.id)])
                if discounts:
                    return {'warning': {'title': _('Warning'), 'message': _(
                        'Already created group wise discount for the supplier '  + rec.supplier.name + "/n If you want make any changes please edit it")}}


class SupplierDiscounts2(models.Model):
    _name = 'supplier.discounts2'
    _rec_name = 'supplier'

    supplier = fields.Many2one('res.partner', 'Supplier')
    lines = fields.One2many(
        comodel_name='list.discount2',
        inverse_name='lists_id',
        string='Set Discounts',
        store=True,
    )

    @api.onchange('supplier')
    def supplier_onchange(self):
        for rec in self:
            if rec.supplier:
                discounts = self.env['supplier.discounts2'].search([('supplier','=',rec.supplier.id)])
                if discounts:
                    return {'warning': {'title': _('Warning'), 'message': _(
                        'Already created product wise discount for the supplier '  + rec.supplier.name + ". If you want to make any changes please edit it")}}


# class SetDiscount2(models.Model):
#     _name = 'set.discount'
#
#     lines = fields.One2many(
#         comodel_name='group.discount',
#         inverse_name='lists_id',
#         string='Set Discounts',
#         store=True,
#     )
#     ac_id = fields.Float('Active ID')
#     test = fields.Many2one('res.partner', 'Test')
#
#     @api.onchange('test')
#     def onchange_ref_id(self):
#         for rec in self:
#             print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<", self.env.context.get('active_id'))
#             self.ac_id = self.env.context.get('active_id')
#
#     @api.one
#     def save_discount(self):
#         pass



class SupplierBillDetails(models.Model):
    _name = 'supplier.bill.details'
    _rec_name = 'inv_sup_no'



    invoice_date=fields.Date('Invoice Date')
    bill_date=fields.Date('Bill Date')
    supplier = fields.Many2one('res.partner', 'Supplier')
    product_of = fields.Many2one('product.medicine.responsible', 'Company')
    amount=fields.Float('Amount')
    inv_sup_no = fields.Char('Invoice No')
    sl_no=fields.Char('SL No')
    discount1=fields.Integer('Discount1')
    discount2=fields.Integer('Discount2')
    GST=fields.Char('GST')
    delivery_charge=fields.Integer('Deliver Charge')
    freight=fields.Integer('Freight To Deduct')
    pay_mode = fields.Selection([('cash', 'Cash'), ('credit', 'Credit'), ('upi', 'UPI'),('cheque','Cheque')], 'Cash Or Credit',
                                default='cash')
    bank_name=fields.Char('Bank Name')
    cheque_no=fields.Char('Chq.No/Transfer No')
    cheque_date=fields.Date('Chq Date')
    delivery_date=fields.Date('Delivery Date')
    total_box=fields.Integer('Total Box')
    remark=fields.Char('Remarks')

    @api.onchange('supplier')
    def gst_no_onchange(self):
        if self.supplier:
            self.GST = self.supplier.gst_number


