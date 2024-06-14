from datetime import datetime

from dateutil.relativedelta import relativedelta

from openerp import models, fields, api


class CustomerInvoiceWizard(models.TransientModel):
    _name = 'customer.wizard'

    partner_id = fields.Many2one('res.partner', 'Customer')
    date_from = fields.Date('Date From')
    date_to = fields.Date('Date To')
    type=fields.Selection([('out_invoice','Sales Invoice'),('packing_slip','Packing Slip'),('holding_invoice','Holding Invoice')])
    invoice_wizard_ids=fields.One2many('account.invoice.wizard','customer_id')

    @api.multi
    def get_details(self):
        self.ensure_one()
        self.invoice_wizard_ids = [(5, 0, 0)]
        if self.date_from and self.date_to:
            domain = [('create_date', '>=', self.date_from),
                      ('create_date', '<=', self.date_to)]
            if self.partner_id:
                domain.append(('partner_id', '=', self.partner_id.id))
            if self.type =='out_invoice':
                domain.append(('invoice_id.type','=','out_invoice'))

            if self.type =='packing_slip':
                domain.append(('invoice_id.packing_invoice', '=', True))

            if self.type =='holding_invoice':
                domain.append(('invoice_id.holding_invoice','=',True))

            invoice_lines = self.env['account.invoice.line'].search(domain)
            line_values = []
            for line in invoice_lines:
                line_values.append((0, 0, {
                    'product_id': line.product_id.id,
                    'quantity': line.quantity or 0.0,
                    'price_unit': line.price_unit or 0.0,
                    'medicine_name_subcat': line.medicine_name_subcat.id if line.medicine_name_subcat else False,
                    'batch':line.batch,
                    'product_of':line.product_of,
                    'medicine_grp':line.medicine_grp,
                    'quantity':line.quantity,
                    'discount':line.discount,
                    'unit_price':line.unit_price,
                    'invoice_line_tax_id4':line.invoice_line_tax_id4,
                    'product_tax':line.product_tax,
                    'price_subtotal':line.price_subtotal,
                    'hsn_code':line.hsn_code,

                }))
            self.update({'invoice_wizard_ids': line_values})
            print(line_values, 'product')
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'customer.wizard',
                'view_mode': 'form',
                'view_type': 'form',
                'res_id': self.id,
                'target': 'new',
            }
class AccountInvoiceLineWizhard(models.TransientModel):
    _name = "account.invoice.wizard"
    _rec_name = 'id'

    customer_id=fields.Many2one('customer.wizard')
    name = fields.Text(string="Description", required=False)
    stock_entry_id = fields.Many2one('entry.stock')
    stock_entry_qty = fields.Float()
    product_id = fields.Many2one('product.product', 'Medicine')
    medicine_name_subcat = fields.Many2one('product.medicine.subcat', 'Potency',)
    batch = fields.Char("Batch", related="product_id.batch")
    medicine_name_packing = fields.Many2one('product.medicine.packing', 'Pack', )
    product_of = fields.Many2one('product.medicine.responsible', 'Company')
    medicine_grp = fields.Many2one('product.medicine.group', 'Grp', )
    stock_transfer_id = fields.Many2one('stock.transfer')
    quantity=fields.Integer('Qty')
    price_unit = fields.Float(string='Mrp')
    unit_price_c = fields.Float(string='Unit price', default=False)
    unit_price = fields.Float(string='Unit price')
    invoice_line_tax_id4 = fields.Float(string='Tax')
    # amount_amount = fields.Float('TAX_AMOUNT', compute="_compute_amount_amount")
    amount_amount = fields.Float('TAX_AMOUNT')
    # amount_amount1 = fields.Float('Tax_amt', compute="_compute_all", store=True)
    # amount_w_tax = fields.Float('TOTAL_AMT', compute="_compute_amount_with_tax")
    amount_w_tax = fields.Float('Total')
    discount = fields.Float(default=0.0)
    discount2 = fields.Float("Dis3(%)")
    discount3 = fields.Float("Dis2(%)", )
    discount4 = fields.Float()
    invoice_id = fields.Many2one('account.invoice', required=False)
    id_for_ref = fields.Integer()
    product_tax = fields.Float('Tax Amt')
    price_subtotal = fields.Float(string='Grand Total',)
    hsn_code = fields.Char('Hsn')




