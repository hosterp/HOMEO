from datetime import datetime

from dateutil.relativedelta import relativedelta

from openerp import models, fields, api


class CustomerInvoiceWizard(models.TransientModel):
    _name = 'customer.wizard'

    partner_id = fields.Many2one('res.partner', 'Customer')
    date_from = fields.Date('Date From')
    date_to = fields.Date('Date To')
    type=fields.Many2one('account.invoice','Type')
    invoice_wizard_ids=fields.One2many('account.invoice.wizard','customer_id')

    @api.multi
    def get_details(self):
        invoice_lines = False
        if self.date_from:
            domain = [('invoice_id.date_invoice', '>=', self.date_from),
                      ('invoice_id.date_invoice', '<=', self.date_to),
                      ('invoice_id.type', '!=', 'out_invoice')]
            if self.partner_id:
                domain += [('partner_id', '=', self.partner_id.id)]
            # if self.company:
            #     domain += [('product_of', '>=', self.company.id)]
            # if self.group:
            #     domain += [('medicine_grp', '>=', self.group.id)]
            # if self.packing:
            #     domain += [('medicine_name_packing', '>=', self.packing.id)]
            # if self.potency:
            #     domain += [('medicine_name_subcat', '>=', self.potency.id)]

            invoice_lines = self.env['account.invoice.line'].search(domain)
            print(invoice_lines,'data')
        return invoice_lines


class AccountInvoiceLineWizhard(models.TransientModel):
    _name = "account.invoice.wizard"
    _rec_name = 'id'

    customer_id=fields.Many2one('customer.wizard')
    name = fields.Text(string="Description", required=False)
    stock_entry_id = fields.Many2one('entry.stock')
    stock_entry_qty = fields.Float()
    product_id = fields.Many2one('product.product', 'Medicine')
    medicine_name_subcat = fields.Many2one('product.medicine.subcat', 'Potency', required=True)
    batch = fields.Char("Batch", related="product_id.batch")
    medicine_name_packing = fields.Many2one('product.medicine.packing', 'Pack', )
    product_of = fields.Many2one('product.medicine.responsible', 'Company')
    medicine_grp = fields.Many2one('product.medicine.group', 'Grp', )
    stock_transfer_id = fields.Many2one('stock.transfer')
    quantity=fields.Integer('Qty')
    price_unit = fields.Float(string='Unit Price')
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




