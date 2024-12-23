# import dateutil.utils
import json

from lxml import etree
from num2words import num2words

from openerp import api, models, fields
from openerp.osv import osv
import openerp.addons.decimal_precision as dp
from openerp.tools.translate import _, _logger
from openerp.exceptions import except_orm, Warning, RedirectWarning, ValidationError
from datetime import datetime
from datetime import date
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import datetime


class AccountAccountInherit(models.Model):
    _inherit = 'account.account'

    medical = fields.Boolean('Medical')


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"
    _rec_name = 'id'

    name = fields.Text(string="Description", required=False)
    stock_entry_id = fields.Many2one('entry.stock')
    stock_entry_qty = fields.Float()
    stock_transfer_id = fields.Many2one('stock.transfer')
    # amount_amount = fields.Float('TAX_AMOUNT', compute="_compute_amount_amount")
    amount_amount = fields.Float('TAX_AMOUNT')
    amount_amount1 = fields.Float('Tax_amt', compute="_compute_all", store=True)
    # amount_w_tax = fields.Float('TOTAL_AMT', compute="_compute_amount_with_tax")
    amount_w_tax = fields.Float('Total')
    discount = fields.Float(default=0.0)
    discount2 = fields.Float("Dis3(%)")
    discount3 = fields.Float("Dis2(%)", )
    discount4 = fields.Float()
    invoice_id = fields.Many2one('account.invoice', required=False)
    id_for_ref = fields.Integer()
    product_tax = fields.Float(compute="_compute_customer_tax")
    unit_price = fields.Float(string='Unit price', compute="_compute_customer_tax", required=False)
    unit_price_s = fields.Float(string='Unit price', required=False, default=False)
    unit_price_c = fields.Float(string='Unit price', required=False,compute="_compute_customer_tax",default=False)
    delete_bool = fields.Boolean(string="Delete", default=False)

    @api.onchange('unit_price_c')
    def _onchange_unit_price_c(self):
        for rec in self:
            if rec.partner_id.customer and rec.price_unit != 0:
                rec.discount = round(100 * ((rec.price_unit - rec.unit_price_c) / rec.price_unit))
            else:
                pass

    @api.onchange('discount3')
    def _onchange_discount3(self):
        for rec in self:
            if rec.partner_id.supplier and rec.unit_price_s != 0:
                rec._compute_all()
            else:
                pass
    @api.onchange('unit_price_s')
    def _onchange_unit_price_s(self):
        for rec in self:
            if rec.partner_id.supplier and rec.unit_price_s != 0:
                price_d1 = self.price_unit * (1 - (self.discount or 0.0) / 100.0)
                # Assuming rec.unit_price_s and price_d1 are defined somewhere
                if price_d1 != 0:
                    discount3_raw = 100 * (price_d1 - rec.unit_price_s) / price_d1
                    discount3_rounded = round(discount3_raw, 2)  # Round to 2 decimal places
                    rec.discount3 = int(discount3_rounded) if discount3_rounded.is_integer() else discount3_rounded
                else:
                    # Handle the case where price_d1 is zero to avoid division by zero error
                    rec.discount3 = None  # Set an appropriate default value or handle it accordingly

            else:
                pass



    @api.model
    def create(self, vals):
        # existing_record = self.search([
        #     ('invoice_id', '=', vals['invoice_id']),
        #     ('product_id', '=', vals['product_id']),
        #     ('expiry_date', '=', vals['expiry_date']),
        #     ('medicine_rack', '=', vals['medicine_rack']),
        #     ('product_of', '=', vals['product_of']),
        #     ('medicine_grp', '=', vals['medicine_grp']),
        #     ('medicine_name_packing', '=', vals['medicine_name_packing']),
        #     ('invoice_line_tax_id4', '=', vals['invoice_line_tax_id4']),
        #     ('medicine_name_subcat', '=', vals['medicine_name_subcat']),
        #     ('price_unit', '=', vals['price_unit']),
        # ], limit=1)
        #
        # if existing_record:
        #     # If similar record exist full_cleared_dbs, update the quantity field instead of creating a new record
        #     existing_record.write({
        #         'quantity': existing_record.quantity + vals.get('quantity', 0)
        #     })
        #     # print(existing_record,'exist')
        #     return existing_record
        result = super(AccountInvoiceLine, self).create(vals)
        # if result.invoice_id.type == 'in_invoice' and result.quantity != 0 and result.medicine_rack and result.price_unit:
        #     vals = {
        #         'supplier_id': result.invoice_id.partner_id.id,
        #         'expiry_date': result.expiry_date,
        #         'manf_date': result.manf_date,
        #         'company': result.product_of.id,
        #         'medicine_1': result.product_id.id,
        #         'potency': result.medicine_name_subcat.id,
        #         'medicine_name_packing': result.medicine_name_packing.id,
        #         'medicine_grp1': result.medicine_grp.id,
        #         'batch_2': result.batch_2.id,
        #         'mrp': result.price_unit,
        #         'qty': result.quantity,
        #         'rack': result.medicine_rack.id,
        #         'hsn_code': result.hsn_code,
        #         'discount': result.discount,
        #         'invoice_line_tax_id4': result.invoice_line_tax_id4,
        #         'stock_date': date.today(),
        #     }
        #     stock_entry = self.env['entry.stock'].create(vals)
        #     result.stock_entry_id = stock_entry.id

        if result.invoice_id.type == 'out_invoice' and result.invoice_id.state == 'packing_slip':
            domain = [
                ('medicine_1', '=', result.product_id.id),
                ('expiry_date', '=', result.expiry_date),
                ('rack', '=', result.medicine_rack.id),
                ('company', '=', result.product_of.id),
                ('medicine_grp1', '=', result.medicine_grp.id),
                ('medicine_name_packing', '=', result.medicine_name_packing.id),
                ('potency', '=', result.medicine_name_subcat.id)
            ]

            entry_stock_ids = self.env['entry.stock'].search(domain, order='id desc')
            if not entry_stock_ids or sum(entry_stock_ids.mapped('qty')) <= 0:
                raise Warning(_('Product with current combination is not available in stock'))

            stock_transfer_id = self.env['stock.transfer'].create({
                'partner_id': result.invoice_id.partner_id.id,
                'title': result.invoice_id.cus_title_1.id,
                'product_id': result.product_id.id,
                'product_uom_qty': result.quantity,
                'date': result.invoice_id.date_invoice
            })
            quantity = result.quantity
            result.stock_transfer_id = stock_transfer_id.id
            stock_entry_qty = 0
            for stock in entry_stock_ids:
                if stock.qty >= quantity:
                    stock.write({
                        'qty': stock.qty - quantity,
                    })
                    stock_entry_qty += quantity
                    break
                else:
                    stock.write({
                        'qty': 0
                    })
                    stock_entry_qty += stock.qty
                quantity -= stock.qty
            result.stock_entry_qty = stock_entry_qty

        return result

    # @api.onchange('medicine_rack')
    # def onchange_medicine_rack(self):
    #     for result in self:
    #         if result.invoice_id.type == 'in_invoice' and result.quantity != 0 and result.price_unit and result.amount_w_tax and result.medicine_rack:
    #             rec = {
    #                 'expiry_date': result.expiry_date,
    #                 'manf_date': result.manf_date,
    #                 'product_of': result.product_of.id,
    #                 'product_id': result.product_id.id,
    #                 'medicine_name_subcat': result.medicine_name_subcat.id,
    #                 'medicine_name_packing': result.medicine_name_packing.id,
    #                 'medicine_grp': result.medicine_grp.id,
    #                 'batch': result.batch,
    #                 'manf_date': result.manf_date,
    #                 'expiry_date': result.expiry_date,
    #                 'price_unit': result.price_unit,
    #                 'quantity': result.quantity,
    #                 'medicine_rack': result.medicine_rack.id,
    #                 'hsn_code': result.hsn_code,
    #                 'invoice_line_tax_id4': result.invoice_line_tax_id4,
    #             }
    #             line_entry = self.env['account.invoice.line'].create(rec)
    #             vals = {
    #                 'supplier_id': result.invoice_id.partner_id.id,
    #                 'expiry_date': result.expiry_date,
    #                 'manf_date': result.manf_date,
    #                 'company': result.product_of.id,
    #                 'medicine_1': result.product_id.id,
    #                 'potency': result.medicine_name_subcat.id,
    #                 'medicine_name_packing': result.medicine_name_packing.id,
    #                 'medicine_grp1': result.medicine_grp.id,
    #                 'batch_2': result.batch_2.id,
    #                 'batch': result.batch,
    #                 'mrp': result.price_unit,
    #                 'qty': result.quantity,
    #                 'rack': result.medicine_rack.id,
    #                 'hsn_code': result.hsn_code,
    #                 'discount': result.discount,
    #                 'invoice_line_tax_id4': result.invoice_line_tax_id4,
    #                 'stock_date': date.today(),
    #                 'invoice_line_id': line_entry.id,
    #             }
    #
    #             stock_entry = self.env['entry.stock'].create(vals)
    #             result.stock_entry_id = stock_entry.id
    @api.onchange('medicine_rack')
    def onchange_medicine_rack(self):
        # Perform necessary updates or field adjustments here
        for result in self:
            if result.invoice_id.type == 'in_invoice' and result.quantity and result.price_unit and result.amount_w_tax and result.medicine_rack:
                # Example of an update that doesn't create new records
                # You can modify the logic here based on your needs
                pass

    def write(self, vals):
        result = super(AccountInvoiceLine, self).write(vals)
        for record in self:
            if record.invoice_id.type == 'in_invoice' and record.quantity and record.price_unit and record.amount_w_tax and record.medicine_rack:
                # Create account.invoice.line record
                rec = {
                    'expiry_date': record.expiry_date,
                    'manf_date': record.manf_date,
                    'product_of': record.product_of.id,
                    'product_id': record.product_id.id,
                    'medicine_name_subcat': record.medicine_name_subcat.id,
                    'medicine_name_packing': record.medicine_name_packing.id,
                    'medicine_grp': record.medicine_grp.id,
                    'batch': record.batch,
                    'price_unit': record.price_unit,
                    'quantity': record.quantity,
                    'medicine_rack': record.medicine_rack.id,
                    'hsn_code': record.hsn_code,
                    'invoice_line_tax_id4': record.invoice_line_tax_id4,
                }
                line_entry = self.env['account.invoice.line'].create(rec)

                # Create entry.stock record
                vals_stock = {
                    'supplier_id': record.invoice_id.partner_id.id,
                    'expiry_date': record.expiry_date,
                    'manf_date': record.manf_date,
                    'company': record.product_of.id,
                    'medicine_1': record.product_id.id,
                    'potency': record.medicine_name_subcat.id,
                    'medicine_name_packing': record.medicine_name_packing.id,
                    'medicine_grp1': record.medicine_grp.id,
                    'batch': record.batch,
                    'mrp': record.price_unit,
                    'qty': record.quantity,
                    'rack': record.medicine_rack.id,
                    'hsn_code': record.hsn_code,
                    'discount': record.discount,
                    'invoice_line_tax_id4': record.invoice_line_tax_id4,
                    'stock_date': date.today(),
                    'invoice_line_id': line_entry.id,
                }
                stock_entry = self.env['entry.stock'].create(vals_stock)

                # Update the stock_entry_id field
                record.write({'stock_entry_id': stock_entry.id})
        return result
    @api.model
    def create(self, vals):
        record = super(AccountInvoiceLine, self).create(vals)
        record._create_stock_entry()
        return record

    def write(self, vals):
        res = super(AccountInvoiceLine, self).write(vals)
        self._create_stock_entry()
        return res

    def _create_stock_entry(self):
        for result in self:
            if result.invoice_id.type == 'in_invoice' and result.quantity != 0 and result.price_unit and result.amount_w_tax and result.medicine_rack:
                rec = {
                    'expiry_date': result.expiry_date,
                    'manf_date': result.manf_date,
                    'product_of': result.product_of.id,
                    'product_id': result.product_id.id,
                    'medicine_name_subcat': result.medicine_name_subcat.id,
                    'medicine_name_packing': result.medicine_name_packing.id,
                    'medicine_grp': result.medicine_grp.id,
                    'batch': result.batch,
                    'manf_date': result.manf_date,
                    'expiry_date': result.expiry_date,
                    'price_unit': result.price_unit,
                    'quantity': result.quantity,
                    'medicine_rack': result.medicine_rack.id,
                    'hsn_code': result.hsn_code,
                    'invoice_line_tax_id4': result.invoice_line_tax_id4,
                }
                line_entry = self.env['account.invoice.line'].create(rec)
                vals = {
                    'supplier_id': result.invoice_id.partner_id.id,
                    'expiry_date': result.expiry_date,
                    'manf_date': result.manf_date,
                    'company': result.product_of.id,
                    'medicine_1': result.product_id.id,
                    'potency': result.medicine_name_subcat.id,
                    'medicine_name_packing': result.medicine_name_packing.id,
                    'medicine_grp1': result.medicine_grp.id,
                    'batch_2': result.batch_2.id,
                    'batch': result.batch,
                    'mrp': result.price_unit,
                    'qty': result.quantity,
                    'rack': result.medicine_rack.id,
                    'hsn_code': result.hsn_code,
                    'discount': result.discount,
                    'invoice_line_tax_id4': result.invoice_line_tax_id4,
                    'stock_date': date.today(),
                    'invoice_line_id': line_entry.id,
                }

                stock_entry = self.env['entry.stock'].create(vals)
                result.stock_entry_id = stock_entry.id

    @api.multi
    def write(self, vals):
        for rec in self:
            if rec.invoice_id.type == 'out_invoice':
                # list_keys = ['product_id', 'expiry_date', 'medicine_rack',
                #              'product_of', 'medicine_grp', 'medicine_name_packing',
                #              'medicine_name_subcat', 'quantity', 'hsn_code']

                # if vals.get('packing_slip') or self.state not in ['draft', 'holding_invoice']:
                if vals.get('packing_slip') or rec.invoice_id.state == 'packing_slip':
                    list_item = ['product_id', 'expiry_date', 'medicine_rack', 'product_of', 'medicine_grp',
                                 'medicine_name_packing', 'medicine_name_subcat', 'quantity', 'hsn_code']
                    flag = 0
                    for item in list_item:
                        if vals.get(item):
                            flag = 1
                    if flag:
                        if vals.get('quantity'):
                            quantity = vals.get('quantity')
                            rec.stock_transfer_id.product_uom_qty = vals.get('quantity')
                        else:
                            quantity = rec.quantity

                        domain = [('qty', '>=', quantity)]
                        if vals.get('product_id'):
                            domain += [('medicine_1', '=', vals.get('product_id'))]
                        else:
                            if rec.product_id:
                                domain += [('medicine_1', '=', rec.product_id.id)]

                        if vals.get('expiry_date'):
                            domain += [('medicine_1', '=', vals.get('expiry_date'))]
                        else:
                            if rec.expiry_date:
                                domain += [('expiry_date', '=', rec.expiry_date)]

                        if vals.get('medicine_rack'):
                            domain += [('medicine_1', '=', vals.get('medicine_rack'))]
                        else:
                            if rec.medicine_rack:
                                domain += [('rack', '=', rec.medicine_rack.id)]

                        if vals.get('product_of'):
                            domain += [('medicine_1', '=', vals.get('product_of'))]
                        else:
                            if rec.product_of:
                                domain += [('company', '=', rec.product_of.id)]

                        if vals.get('medicine_grp'):
                            domain += [('medicine_1', '=', vals.get('medicine_grp'))]
                        else:
                            if rec.medicine_grp:
                                domain += [('medicine_grp1', '=', rec.medicine_grp.id)]

                        if vals.get('medicine_name_packing'):
                            domain += [('medicine_1', '=', vals.get('medicine_name_packing'))]
                        else:
                            if rec.medicine_name_packing:
                                domain += [('medicine_name_packing', '=', rec.medicine_name_packing.id)]

                        if vals.get('medicine_name_subcat'):
                            domain += [('medicine_1', '=', vals.get('medicine_name_subcat'))]
                        else:
                            if rec.medicine_name_subcat:
                                domain += [('potency', '=', rec.medicine_name_subcat.id)]

                        if vals.get('hsn_code'):
                            domain += [('medicine_1', '=', vals.get('hsn_code'))]
                        else:
                            if rec.hsn_code:
                                domain += [('hsn_code', '=', rec.hsn_code)]
                        # domain += [('qty', '=', 0)]
                        entry_stock_ids = rec.env['entry.stock'].search(domain, order='id asc', limit=1)
                        if sum(entry_stock_ids.mapped('qty')) <= 0 or not entry_stock_ids:
                            if vals.get('medicine_rack'):
                                domain.remove(('rack', '=', vals.get('medicine_rack')))
                            if rec.medicine_rack:
                                domain.remove(('rack', '=', rec.medicine_rack.id))
                            if rec.expiry_date:
                                domain.remove(('expiry_date', '=', rec.expiry_date))
                            if vals.get('expiry_date'):
                                domain.remove(('expiry_date', '=', vals.get('expiry_date')))
                            entry_stock_ids = rec.env['entry.stock'].search(domain, order='id asc')
                        if not entry_stock_ids:
                            domain.remove(('qty', '>=', quantity))
                            domain += [('qty', '>=', 0)]
                            entry_stock_ids = rec.env['entry.stock'].search(domain, order='id asc')

                        if sum(entry_stock_ids.mapped('qty')) <= 0 or not entry_stock_ids:
                            raise Warning(
                                _('Only we have %s Products with current combination in stock') % str(
                                    int(rec.stock_entry_qty) + int(sum(entry_stock_ids.mapped('qty')))))
                        quantity_comp = quantity
                        inverse = False
                        if rec.stock_entry_qty < quantity:
                            quantity_comp = vals.get('quantity') - rec.stock_entry_qty
                        else:
                            quantity_comp = rec.stock_entry_qty - vals.get('quantity')
                            inverse = True
                        for stock in entry_stock_ids:
                            if quantity_comp > 0:
                                if stock.qty >= quantity_comp:
                                    if inverse:
                                        stock.write({
                                            'qty': abs(stock.qty + quantity_comp),
                                        })
                                    else:
                                        stock.write({
                                            'qty': abs(stock.qty - quantity_comp),
                                        })
                                    # quantity -= stock.qty
                                    break
                                else:
                                    quantity_comp = (quantity_comp - stock.qty)
                                    stock.write({
                                        'qty': 0
                                    })
                        vals['stock_entry_qty'] = quantity
            res = super(AccountInvoiceLine, rec).write(vals)
            # if rec.invoice_id.type == 'in_invoice':
            #     vals = {
            #         'supplier_id': rec.invoice_id.partner_id.id,
            #         'expiry_date': rec.expiry_date,
            #         'manf_date': rec.manf_date,
            #         'company': rec.product_of.id,
            #         'medicine_1': rec.product_id.id,
            #         'potency': rec.medicine_name_subcat.id,
            #         'medicine_name_packing': rec.medicine_name_packing.id,
            #         'medicine_grp1': rec.medicine_grp.id,
            #         'batch_2': rec.batch_2.id,
            #         'mrp': rec.price_unit,
            #         'qty': rec.quantity,
            #         'rack': rec.medicine_rack.id,
            #         'hsn_code': rec.hsn_code,
            #         'discount': rec.discount,
            #         'invoice_line_tax_id4': rec.invoice_line_tax_id4,
            #     }
            #     result = rec.stock_entry_id.write(vals)
            return res



    @api.multi
    def unlink(self):
        for rec in self:
            if rec.invoice_id.state in ['draft', 'holding_invoice', 'packing_slip']:
                if rec.invoice_id.type == 'in_invoice':
                    # if rec.stock_entry_id:
                    #     rec.stock_entry_id.unlink()
                    print("hiaiiii")
                if rec.invoice_id.type == 'out_invoice':
                    if rec.invoice_id.packing_slip:
                        if rec.stock_entry_qty:
                            domain = []
                            if rec.product_id:
                                domain += [('medicine_1', '=', rec.product_id.id)]
                            if rec.expiry_date:
                                domain += [('expiry_date', '=', rec.expiry_date)]
                            if rec.medicine_rack:
                                domain += [('rack', '=', rec.medicine_rack.id)]
                            if rec.product_of:
                                domain += [('company', '=', rec.product_of.id)]
                            if rec.medicine_grp:
                                domain += [('medicine_grp1', '=', rec.medicine_grp.id)]
                            if rec.medicine_name_packing:
                                domain += [('medicine_name_packing', '=', rec.medicine_name_packing.id)]
                            if rec.medicine_name_subcat:
                                domain += [('potency', '=', rec.medicine_name_subcat.id)]
                            entry_stock_id = self.env['entry.stock'].search(domain, order='id desc', limit=1)
                            if not entry_stock_id:
                                if rec.medicine_rack:
                                    domain -= [('rack', '=', self.medicine_rack.id)]
                                    entry_stock_id = self.env['entry.stock'].search(domain, order='id desc', limit=1)
                            entry_stock_id.write({
                                'qty': entry_stock_id.qty + rec.quantity,
                            })
            else:
                raise Warning("Only Draft Invoice Lines can be deleted")
        return super(AccountInvoiceLine, self).unlink()

    # CALCULATE CATEGORY DISCOUNT-CUSTOMER INVOICE
    @api.one
    @api.depends('discount', 'calc')
    def _compute_mass_discount(self):
        if self.invoice_id.discount_rate == 0:
            pass
        # else:
        #     if self.discount == 0:
        #         discount_rate = self.invoice_id.discount_rate
        #         self.discount = discount_rate

    @api.model
    def move_line_get_item(self, line):
        total_price = 0
        if line.invoice_id.type in ('out_invoice'):
            total_price = round(line.price_subtotal)
            # total_price = line.amt_w_tax
            if line.invoice_id.advance_amount:
                if line.invoice_id.advance_amount > total_price:
                    if line.invoice_id.advance_amount == total_price:
                        line.invoice_id.partner_id.advance_amount = 0
                        total_price = 0
                    else:
                        line.invoice_id.partner_id.advance_amount -= total_price
                        total_price = 0
                else:
                    total_price -= line.invoice_id.advance_amount
                    line.invoice_id.partner_id.advance_amount = 0
            else:
                pass
        if line.invoice_id.type != ('out_invoice', 'out_refund'):
            # total_price = line.amount_w_tax
            discount = line.quantity * line.price_unit * (line.discount / 100)
            amount = (line.quantity * line.price_unit) - discount
            tax_amount = amount * (line.invoice_line_tax_id4 / 100)
            total_price = line.amount_w_tax

        return {
            'type': 'src',
            'name': line.name,
            'price_unit': line.price_unit,
            'quantity': line.quantity,
            'price': total_price or line.price_subtotal,
            'account_id': line.account_id.id,
            'product_id': line.product_id.id,
            'uos_id': line.uos_id.id,
            'account_analytic_id': line.account_analytic_id.id,
            'taxes': line.invoice_line_tax_id,
        }

    # @api.model
    # def move_line_get(self, invoice_id):
    #     res = []
    #     self._cr.execute(
    #         'SELECT * FROM account_invoice_tax WHERE invoice_id = %s',
    #         (invoice_id,)
    #     )
    #     for row in self._cr.dictfetchall():
    #         if not (row['amount'] or row['tax_code_id'] or row['tax_amount']):
    #             continue
    #         res.append({
    #             'type': 'tax',
    #             'name': row['name'],
    #             'price_unit': row['amount'],
    #             'quantity': 1,
    #             'price': row['amount'] or 0.0,
    #             'account_id': row['account_id'],
    #             'tax_code_id': row['tax_code_id'],
    #             'tax_amount': row['tax_amount'],
    #             'account_analytic_id': row['account_analytic_id'],
    #         })
    #     return res

    # CUSTOMER TAX CALCULATION
    @api.model
    @api.depends('amt_w_tax', 'invoice_line_tax_id4', 'price_subtotal', 'amount_amount1', 'price_unit', 'rate_amtc',
                 'product_tax', 'unit_price', 'unit_price_s')
    def _compute_customer_tax(self):
        for record in self:
            if record.partner_id.customer:
                if record.invoice_id.gst_type == 'gst_minus':
                    for rec in record:
                        if rec.rate_amtc == 0:
                            if rec.rate_amtc < rec.price_subtotal:
                                if rec.rate_amtc == 0:
                                    rate_amount = rec.price_subtotal
                                    quantity = rec.quantity
                                    per_product = round(rate_amount / quantity, 2)
                                    perce = rec.invoice_line_tax_id4
                                    tax_amount = round(perce * 100 / (perce + 100), 2)
                                    tax = round(per_product * tax_amount / 100, 2)
                                    rec.product_tax = round(tax * quantity, 2)
                                    rec.unit_price = round(per_product - tax, 2)
                                    rec.unit_price_c = round(per_product, 2)
                                    rec.amt_tax = round(rec.product_tax, 2)
                                    rec.amt_w_tax = round(rec.price_subtotal, 2)
                                    rec.amount_residual = round(rec.price_subtotal, 2)
                                    rec.amount_residual_currency = round(rec.price_subtotal, 2)
                        else:
                            rate_amount = rec.price_subtotal
                            quantity = rec.quantity
                            per_product = round(rate_amount / quantity, 2)
                            perce = rec.invoice_line_tax_id4
                            tax_amount = round(perce * 100 / (perce + 100), 2)
                            tax = round(per_product * tax_amount / 100, 2)
                            rec.product_tax = round(tax * quantity, 2)
                            rec.unit_price = round(per_product - tax, 2)
                            rec.unit_price_c = round(per_product, 2)
                            rec.amt_tax = round(rec.product_tax, 2)
                            rec.amt_w_tax = round(rec.price_subtotal, 2)
                            rec.amount_residual = round(rec.price_subtotal, 2)
                            rec.amount_residual_currency = round(rec.price_subtotal, 2)
                            # perce = rec.invoice_line_tax_id4
                            # new_rate = rec.rate_amtc
                            # tax = new_rate * (perce / 100)
                            # rec.amt_tax = round(tax)
                            # total = new_rate + round(tax)
                            # rec.amt_w_tax = total
                else:
                    for rec in record:
                        if rec.rate_amtc == 0:
                            if rec.rate_amtc < rec.price_subtotal:
                                if rec.rate_amtc == 0:
                                    rate_amount = rec.price_subtotal
                                    quantity = rec.quantity
                                    per_product = round(rate_amount / quantity, 2)
                                    perce = rec.invoice_line_tax_id4
                                    tax_amount = round(perce * 100 / (perce + 100), 2)
                                    tax = round(per_product * tax_amount / 100, 2)
                                    rec.product_tax = round(tax * quantity, 2)
                                    rec.unit_price = round(per_product, 2)
                                    rec.unit_price_c = round(per_product, 2)
                                    rec.amt_tax = round(rec.product_tax, 2)
                                    rec.amt_w_tax = round(rec.price_subtotal, 2)
                                    rec.amount_residual = round(rec.price_subtotal, 2)
                                    rec.amount_residual_currency = round(rec.price_subtotal, 2)
                        else:
                            rate_amount = rec.price_subtotal
                            quantity = rec.quantity
                            per_product = round(rate_amount / quantity, 2)
                            perce = rec.invoice_line_tax_id4
                            tax_amount = round(perce * 100 / (perce + 100), 2)
                            tax = round(per_product * tax_amount / 100, 2)
                            rec.product_tax = round(tax * quantity, 2)
                            rec.unit_price = round(per_product, 2)
                            rec.unit_price_c = round(per_product, 2)
                            rec.amt_tax = round(rec.product_tax, 2)
                            rec.amt_w_tax = round(rec.price_subtotal, 2)
                            rec.amount_residual = round(rec.price_subtotal, 2)
                            rec.amount_residual_currency = round(rec.price_subtotal, 2)
                            # perce = rec.invoice_line_tax_id4
                            # new_rate = rec.rate_amtc
                            # tax = new_rate * (perce / 100)
                            # rec.amt_tax = round(tax)
                            # total = new_rate + round(tax)
                            # rec.amt_w_tax = total

    @api.one
    @api.depends('product_id', 'medicine_name_subcat', 'medicine_grp', 'medicine_name_subcat',
                 'price_unit','discount3','discount2','unit_price_s',
                 'quantity', 'discount')
    def _compute_all(self):
        if self.partner_id.supplier == True:
            # FETCH DISCOUNT1
            for rec in self:
                if rec.medicine_grp.id and rec.product_of.id and rec.product_id.id and rec.medicine_name_subcat.id and rec.medicine_name_packing.id:
                    flag = 0
                    s_obj = self.env['supplier.discounts'].search([('supplier', '=', rec.partner_id.id)])
                    if s_obj:
                        for lines in s_obj.lines:
                            if (lines.medicine_grp1.id == rec.medicine_grp.id and lines.company.id == rec.product_of.id and lines.medicine_1.id == rec.product_id.id
                                    and lines.potency.id == rec.medicine_name_subcat.id and lines.medicine_name_packing.id == rec.medicine_name_packing.id):
                                rec.discount = lines.discount
                                flag = 1
                                break
                            else:
                                pass
                            if (lines.medicine_grp1.id == rec.medicine_grp.id and lines.company.id == rec.product_of.id and lines.medicine_1.id == rec.product_id.id
                                    and lines.potency.id == rec.medicine_name_subcat.id and lines.medicine_name_packing.id == False):
                                rec.discount = lines.discount
                                flag = 1
                                break
                            else:
                                pass
                            if (lines.medicine_grp1.id == rec.medicine_grp.id and lines.company.id == rec.product_of.id and lines.medicine_1.id == rec.product_id.id
                                    and lines.potency.id == False and lines.medicine_name_packing.id == rec.medicine_name_packing.id):
                                rec.discount = lines.discount
                                flag = 1
                                break
                            else:
                                pass
                            if (lines.medicine_grp1.id == rec.medicine_grp.id and lines.company.id == rec.product_of.id and lines.medicine_1.id == False
                                    and lines.medicine_name_packing.id == rec.medicine_name_packing.id and lines.potency.id == rec.medicine_name_subcat.id):
                                rec.discount = lines.discount
                                flag = 1
                                break
                            else:
                                pass
                            if (lines.medicine_grp1.id == rec.medicine_grp.id and lines.company.id == rec.product_of.id and lines.medicine_1.id == rec.product_id.id
                                    and lines.medicine_name_packing.id == False and lines.potency.id == False):
                                rec.discount = lines.discount
                                flag = 1
                                break
                            else:
                                pass
                            if (lines.medicine_grp1.id == rec.medicine_grp.id and lines.company.id == rec.product_of.id and lines.potency.id == rec.medicine_name_subcat.id
                                    and lines.medicine_1.id == False and lines.medicine_name_packing.id == False):
                                rec.discount = lines.discount
                                flag = 1
                                break
                            else:
                                pass
                            if (lines.medicine_grp1.id == rec.medicine_grp.id and lines.company.id == rec.product_of.id
                                    and lines.medicine_name_packing.id == rec.medicine_name_packing.id and lines.medicine_1.id == False and lines.potency.id == False):
                                rec.discount = lines.discount
                                flag = 1
                                break
                            else:
                                pass
                            if (lines.medicine_grp1.id == rec.medicine_grp.id and lines.company.id == rec.product_of.id
                                    and lines.medicine_1.id == False and lines.medicine_name_packing.id == False and lines.potency.id == False):
                                rec.discount = lines.discount
                                flag = 1
                                break
                            else:
                                rec.discount = 0
                                # raise Warning("No Supplier Discount Available")
            # FETCH EXTRA DDISCOUNT
            if self.medicine_grp and not self.discount3:
                dis_obj = self.env['group.discount'].search([('medicine_grp', '=', self.medicine_grp.id),
                                                             (
                                                                 'medicine_name_subcat', '=',
                                                                 self.medicine_name_subcat.id),
                                                             ('medicine_name_packing', '=',
                                                              self.medicine_name_packing.id)])
                if dis_obj:
                    varia = dis_obj.discount
                    self.discount3 = dis_obj.discount
                    if dis_obj.expiry_months:
                        if self.manf_date:
                            text = self.manf_date
                            x = datetime.strptime(text, '%Y-%m-%d')
                            nextday_date = x + relativedelta(months=dis_obj.expiry_months)
                            cal_date = datetime.strftime(nextday_date, '%Y-%m-%d')
                            # print("calculated date............", cal_date)
                            self.expiry_date = cal_date
                            # self.write({'expiry_date': cal_date})
                else:
                    dis_obj2 = self.env['group.discount'].search([('medicine_grp', '=', self.medicine_grp.id),
                                                                  ('medicine_name_subcat', '=',
                                                                   self.medicine_name_subcat.id),
                                                                  ('medicine_name_packing', '=', None)])

                    if dis_obj2:
                        self.discount3 = dis_obj2.discount
                        if dis_obj2.expiry_months:
                            if self.manf_date:
                                text = self.manf_date
                                x = datetime.strptime(text, '%Y-%m-%d')
                                nextday_date = x + relativedelta(months=dis_obj2.expiry_months)
                                cal_date = datetime.strftime(nextday_date, '%Y-%m-%d')
                                self.expiry_date = cal_date
                                # self.write({'expiry_date': cal_date})
                    else:
                        dis_obj4 = self.env['group.discount'].search([('medicine_grp', '=', self.medicine_grp.id),
                                                                      ('medicine_name_subcat', '=', None),
                                                                      ('medicine_name_packing', '=',
                                                                       self.medicine_name_packing.id)])
                        if dis_obj4:
                            self.discount3 = dis_obj4.discount
                            if dis_obj4.expiry_months:
                                if self.manf_date:
                                    text = self.manf_date
                                    x = datetime.strptime(text, '%Y-%m-%d')
                                    nextday_date = x + relativedelta(months=dis_obj4.expiry_months)
                                    cal_date = datetime.strftime(nextday_date, '%Y-%m-%d')
                                    self.expiry_date = cal_date
                                    # self.write({'expiry_date': cal_date})


                        else:
                            dis_obj3 = self.env['group.discount'].search([('medicine_grp', '=', self.medicine_grp.id),
                                                                          ('medicine_name_subcat', '=', None),
                                                                          ('medicine_name_packing', '=', None)])
                            if dis_obj3:
                                self.discount3 = dis_obj3.discount
                                if dis_obj3.expiry_months:
                                    if self.manf_date:
                                        text = self.manf_date
                                        x = datetime.strptime(text, '%Y-%m-%d')
                                        nextday_date = x + relativedelta(months=dis_obj3.expiry_months)
                                        cal_date = datetime.strftime(nextday_date, '%Y-%m-%d')
                                        self.expiry_date = cal_date
                                        # self.write({'expiry_date': cal_date})
                            else:
                                dis_obj2 = self.env['group.discount'].search(
                                    [('medicine_grp', '=', None),
                                     ('medicine_name_subcat', '=',
                                      self.medicine_name_subcat.id),
                                     ('medicine_name_packing', '=', None)])

                                if dis_obj2:
                                    self.discount3 = dis_obj2.discount
                                    if dis_obj2.expiry_months:
                                        if self.manf_date:
                                            text = self.manf_date
                                            x = datetime.strptime(text, '%Y-%m-%d')
                                            nextday_date = x + relativedelta(months=dis_obj2.expiry_months)
                                            cal_date = datetime.strftime(nextday_date, '%Y-%m-%d')
                                            self.expiry_date = cal_date
                                            # self.write({'expiry_date': cal_date})
                                else:
                                    pass
            else:
                pass
            # TAX CALCULATION AND SUBTOTAL WITH 2 DISCOUNTS IF THERE IS DISCOUNT1 AND DISCOUNT2
            if self.price_unit:
                subtotal_wo_dis1 = round(self.price_unit * self.quantity, 2)
                if rec.discount:
                    if rec.discount3:
                        d1 = round(self.price_unit * (self.discount / 100), 2)
                        total_d1 = round(d1 * self.quantity, 2)
                        self.dis1 = total_d1
                        unit_price = round(self.price_unit - d1, 2)

                        # Discount 2 calculation
                        d2 = round(unit_price * (self.discount3 / 100), 2)
                        total_d2 = round(d2 * rec.quantity, 2)
                        self.dis2 = total_d2
                        unit_price -= d2
                        if self.discount2:
                            d3 = round(unit_price * (self.discount2 / 100), 2)
                            total_d3 = round(d3 * rec.quantity, 2)
                            unit_price -= d3
                            # Tax calculation
                            single_tax = round(unit_price * (self.invoice_line_tax_id4 / 100), 2)
                            total_tax = round(single_tax * self.quantity, 2)
                            self.amount_amount1 = total_tax

                            self.rate_amt = round(unit_price * self.quantity, 2)
                            self.unit_price_s = round(unit_price, 2)
                            final_price = round(self.unit_price_s * self.quantity, 2)
                            self.price_subtotal = final_price
                            self.amount_w_tax = round(final_price + total_tax, 2)
                            self.grand_total = round(final_price + total_tax, 2)
                        else:
                            # Tax calculation
                            single_tax = round(unit_price * (self.invoice_line_tax_id4 / 100), 2)
                            total_tax = round(single_tax * self.quantity, 2)
                            self.amount_amount1 = total_tax

                            self.rate_amt = round(unit_price * self.quantity, 2)
                            self.unit_price_s = round(unit_price, 2)
                            final_price = round(self.unit_price_s * self.quantity, 2)
                            self.price_subtotal = final_price
                            self.amount_w_tax = round(final_price + total_tax, 2)
                            self.grand_total = round(final_price + total_tax, 2)

                    else:
                        # Discount 1 calculation
                        d1 = round(self.price_unit * (self.discount / 100), 2)
                        total_d1 = round(d1 * self.quantity, 2)
                        self.dis1 = total_d1
                        unit_price = round(self.price_unit - d1, 2)

                        if self.discount2:
                            d3 = round(unit_price * (self.discount2 / 100), 2)
                            total_d3 = round(d3 * rec.quantity, 2)
                            unit_price -= d3

                            # Tax calculation
                            single_tax = round(unit_price * (self.invoice_line_tax_id4 / 100), 2)
                            total_tax = round(single_tax * self.quantity, 2)
                            self.amount_amount1 = total_tax
                            self.dis2 = 0
                            self.rate_amt = round(unit_price * self.quantity, 2)
                            self.unit_price_s = round(unit_price, 2)
                            final_price = round(self.unit_price_s * self.quantity, 2)
                            self.price_subtotal = final_price
                            self.amount_w_tax = round(final_price + total_tax, 2)
                            self.grand_total = round(final_price + total_tax, 2)
                        else:
                            # Tax calculation
                            single_tax = round(unit_price * (self.invoice_line_tax_id4 / 100), 2)
                            total_tax = round(single_tax * self.quantity, 2)
                            self.amount_amount1 = total_tax
                            self.dis2 = 0
                            self.rate_amt = round(unit_price * self.quantity, 2)
                            self.unit_price_s = round(unit_price, 2)
                            final_price = round(self.unit_price_s * self.quantity, 2)
                            self.price_subtotal = final_price
                            self.amount_w_tax = round(final_price + total_tax, 2)
                            self.grand_total = round(final_price + total_tax, 2)
                else:
                    if rec.discount3:
                        # Discount 2 calculation
                        d2 = round(self.price_unit * (self.discount3 / 100), 2)
                        total_d2 = round(d2 * self.quantity, 2)
                        self.dis2 = total_d2
                        self.dis1 = 0
                        unit_price = round(self.price_unit - d2, 2)

                        if self.discount2:
                            d3 = round(unit_price * (self.discount2 / 100), 2)
                            total_d3 = round(d3 * rec.quantity, 2)
                            unit_price -= d3

                            # Tax calculation
                            single_tax = round(unit_price * (self.invoice_line_tax_id4 / 100), 2)
                            total_tax = round(single_tax * self.quantity, 2)
                            self.amount_amount1 = total_tax

                            self.rate_amt = round(unit_price * self.quantity, 2)
                            self.unit_price_s = round(unit_price, 2)
                            final_price = round(self.unit_price_s * self.quantity, 2)
                            self.price_subtotal = final_price
                            self.amount_w_tax = round(final_price + total_tax, 2)
                            self.grand_total = round(final_price + total_tax, 2)
                        else:
                            # Tax calculation
                            single_tax = round(unit_price * (self.invoice_line_tax_id4 / 100), 2)
                            total_tax = round(single_tax * self.quantity, 2)
                            self.amount_amount1 = total_tax

                            self.rate_amt = round(unit_price * self.quantity, 2)
                            self.unit_price_s = round(unit_price, 2)
                            final_price = round(self.unit_price_s * self.quantity, 2)
                            self.price_subtotal = final_price
                            self.amount_w_tax = round(final_price + total_tax, 2)
                            self.grand_total = round(final_price + total_tax, 2)
                    else:
                        self.dis2 = 0
                        self.dis1 = 0
                        unit_price = round(self.price_unit, 2)

                        if self.discount2:
                            d3 = round(unit_price * (self.discount2 / 100), 2)
                            total_d3 = round(d3 * rec.quantity, 2)
                            unit_price -= d3

                            # Tax calculation
                            single_tax = round(unit_price * (self.invoice_line_tax_id4 / 100), 2)
                            total_tax = round(single_tax * self.quantity, 2)
                            self.amount_amount1 = total_tax

                            self.rate_amt = round(unit_price * self.quantity, 2)
                            self.unit_price_s = round(unit_price, 2)
                            final_price = round(self.unit_price_s * self.quantity, 2)
                            self.price_subtotal = final_price
                            self.amount_w_tax = round(final_price + total_tax, 2)
                            self.grand_total = round(final_price + total_tax, 2)
                        else:
                            # Tax calculation
                            single_tax = round(unit_price * (self.invoice_line_tax_id4 / 100), 2)
                            total_tax = round(single_tax * self.quantity, 2)
                            self.amount_amount1 = total_tax

                            self.rate_amt = round(unit_price * self.quantity, 2)
                            self.unit_price_s = round(unit_price, 2)
                            final_price = round(self.unit_price_s * self.quantity, 2)
                            self.price_subtotal = final_price
                            self.amount_w_tax = round(final_price + total_tax, 2)
                            self.grand_total = round(final_price + total_tax, 2)


            # self.grand_total = self.amount_w_tax - self.amount_amount1
            # print("finallyyyyy", self.rate_amt)

    # @api.one
    # @api.depends('product_id', 'medicine_name_subcat', 'medicine_grp', 'medicine_name_subcat', 'discount2',
    #              'price_unit',
    #              'quantity', 'discount')
    # def _compute_all(self):
    #     if self.partner_id.supplier == True:
    #         # FETCH DISCOUNT1
    #         for rec in self:
    #             flag = 0
    #             s_obj = self.env['supplier.discounts'].search([('supplier', '=', rec.partner_id.id)])
    #             if s_obj:
    #                 for lines in s_obj.lines:
    #                     if (lines.company.id == rec.product_of.id):
    #                         if (lines.medicine_1.id == rec.product_id.id):
    #                             if (lines.potency.id == rec.medicine_name_subcat.id):
    #                                 if (lines.medicine_grp1.id == rec.medicine_grp.id):
    #                                     if (lines.medicine_name_packing.id == rec.medicine_name_packing.id):
    #                                         rec.discount = lines.discount
    #                                         flag = 1
    #                     if flag == 1:
    #                         pass
    #                     else:
    #
    #                         # print("Search in 2nd model")
    #                         s_obj = self.env['supplier.discounts2'].search([('supplier', '=', rec.partner_id.id)])
    #                         if s_obj:
    #                             for lines in s_obj.lines:
    #                                 if (lines.company.id == rec.product_of.id):
    #                                     # if (lines.medicine_1.id == rec.product_id.id):
    #                                     if (lines.potency.id == rec.medicine_name_subcat.id):
    #                                         if (lines.medicine_grp1.id == rec.medicine_grp.id):
    #                                             if (lines.medicine_name_packing.id == rec.medicine_name_packing.id):
    #                                                 rec.discount = lines.discount
    #                                                 print("success")
    #
    #                                 # if ((lines.company.id == rec.product_of.id) and (
    #                                 #         lines.medicine_grp1.id == rec.medicine_grp.id) and (
    #                                 #         lines.medicine_1.id == None) and (
    #                                 #         lines.potency.id == rec.medicine_name_subcat.id) and (
    #                                 #         lines.medicine_name_packing.id == rec.medicine_name_packing.id)):
    #                                 #     rec.discount = lines.discount
    #                                 # else:
    #                                 if ((lines.company.id == rec.product_of.id) and (
    #                                         lines.medicine_grp1.id == rec.medicine_grp.id)
    #                                         and (
    #                                                 lines.potency.id == rec.medicine_name_subcat.id) and (
    #                                                 lines.medicine_name_packing.id == None)):
    #                                     rec.discount = lines.discount
    #                                 else:
    #                                     if ((lines.company.id == rec.product_of.id) and (
    #                                             lines.medicine_grp1.id == rec.medicine_grp.id) and (
    #                                             lines.potency.id == None) and (
    #                                             lines.medicine_name_packing.id == rec.medicine_name_packing.id)):
    #                                         rec.discount = lines.discount
    #                                     else:
    #                                         if ((lines.company.id == rec.product_of.id) and (
    #                                                 lines.medicine_grp1.id == rec.medicine_grp.id) and (
    #                                                 lines.potency.id == None) and (
    #                                                 lines.medicine_name_packing.id == None)):
    #                                             rec.discount = lines.discount
    #                                         if ((lines.company.id == rec.product_of.id) and (
    #                                                 lines.medicine_name_packing.id == None) and (
    #                                                 lines.potency.id == None) and (
    #                                                 lines.medicine_grp1.id == rec.medicine_grp.id)):
    #                                             rec.discount = lines.discount
    #                                         if ((lines.company.id == None) and (
    #                                                 lines.medicine_name_packing.id == rec.medicine_name_packing.id) and (
    #                                                 lines.potency.id == rec.medicine_name_subcat.id) and (
    #                                                 lines.medicine_grp1.id == None)):
    #                                             rec.discount = lines.discount
    #                                         if ((lines.company.id == None) and (
    #                                                 lines.medicine_name_packing.id == None) and (
    #                                                 lines.potency.id == None) and (
    #                                                 lines.medicine_grp1.id == rec.medicine_grp.id)):
    #                                             rec.discount = lines.discount
    #                                         if ((lines.company.id == None) and (
    #                                                 lines.medicine_name_packing.id == None) and (
    #                                                 lines.potency.id == rec.medicine_name_subcat.id) and (
    #                                                 lines.medicine_grp1.id == None)):
    #                                             rec.discount = lines.discount
    #                                         if ((lines.company.id == None) and (
    #                                                 lines.medicine_name_packing.id == rec.medicine_name_packing.id) and (
    #                                                 lines.potency.id == None) and (lines.medicine_grp1.id == None)):
    #                                             rec.discount = lines.discount
    #
    #         # FETCH EXTRA DDISCOUNT
    #         if self.medicine_grp:
    #             dis_obj = self.env['group.discount'].search([('medicine_grp', '=', self.medicine_grp.id),
    #                                                          (
    #                                                              'medicine_name_subcat', '=',
    #                                                              self.medicine_name_subcat.id),
    #                                                          ('medicine_name_packing', '=',
    #                                                           self.medicine_name_packing.id)])
    #             if dis_obj:
    #                 varia = dis_obj.discount
    #                 self.discount3 = dis_obj.discount
    #                 if dis_obj.expiry_months:
    #                     if self.manf_date:
    #                         text = self.manf_date
    #                         x = datetime.strptime(text, '%Y-%m-%d')
    #                         nextday_date = x + relativedelta(months=dis_obj.expiry_months)
    #                         cal_date = datetime.strftime(nextday_date, '%Y-%m-%d')
    #                         # print("calculated date............", cal_date)
    #                         self.expiry_date = cal_date
    #                         # self.write({'expiry_date': cal_date})
    #             else:
    #                 dis_obj2 = self.env['group.discount'].search([('medicine_grp', '=', self.medicine_grp.id),
    #                                                               ('medicine_name_subcat', '=',
    #                                                                self.medicine_name_subcat.id),
    #                                                               ('medicine_name_packing', '=', None)])
    #
    #                 if dis_obj2:
    #                     self.discount3 = dis_obj2.discount
    #                     if dis_obj2.expiry_months:
    #                         if self.manf_date:
    #                             text = self.manf_date
    #                             x = datetime.strptime(text, '%Y-%m-%d')
    #                             nextday_date = x + relativedelta(months=dis_obj2.expiry_months)
    #                             cal_date = datetime.strftime(nextday_date, '%Y-%m-%d')
    #                             self.expiry_date = cal_date
    #                             # self.write({'expiry_date': cal_date})
    #                 else:
    #                     dis_obj4 = self.env['group.discount'].search([('medicine_grp', '=', self.medicine_grp.id),
    #                                                                   ('medicine_name_subcat', '=', None),
    #                                                                   ('medicine_name_packing', '=',
    #                                                                    self.medicine_name_packing.id)])
    #                     if dis_obj4:
    #                         self.discount3 = dis_obj4.discount
    #                         if dis_obj4.expiry_months:
    #                             if self.manf_date:
    #                                 text = self.manf_date
    #                                 x = datetime.strptime(text, '%Y-%m-%d')
    #                                 nextday_date = x + relativedelta(months=dis_obj4.expiry_months)
    #                                 cal_date = datetime.strftime(nextday_date, '%Y-%m-%d')
    #                                 self.expiry_date = cal_date
    #                                 # self.write({'expiry_date': cal_date})
    #
    #
    #                     else:
    #                         dis_obj3 = self.env['group.discount'].search([('medicine_grp', '=', self.medicine_grp.id),
    #                                                                       ('medicine_name_subcat', '=', None),
    #                                                                       ('medicine_name_packing', '=', None)])
    #                         if dis_obj3:
    #                             self.discount3 = dis_obj3.discount
    #                             if dis_obj3.expiry_months:
    #                                 if self.manf_date:
    #                                     text = self.manf_date
    #                                     x = datetime.strptime(text, '%Y-%m-%d')
    #                                     nextday_date = x + relativedelta(months=dis_obj3.expiry_months)
    #                                     cal_date = datetime.strftime(nextday_date, '%Y-%m-%d')
    #                                     self.expiry_date = cal_date
    #                                     # self.write({'expiry_date': cal_date})
    #
    #         # TAX CALCULATION AND SUBTOTAL WITH 2 DISCOUNTS IF THERE IS DISCOUNT1 AND DISCOUNT2
    #         if self.price_unit:
    #             # print("price unit exist")
    #             subtotal_wo_dis1 = self.price_unit * self.quantity
    #             if self.discount:
    #                 # print("first discount exist")
    #                 if self.discount3:
    #                     # print("condition-extra discount")
    #                     discount1_amount = subtotal_wo_dis1 * (self.discount / 100)
    #                     item = self.invoice_line_tax_id4
    #                     subtotal_with_dis1 = subtotal_wo_dis1 - discount1_amount
    #                     tax_amount = subtotal_with_dis1 * (item / 100)
    #                     # self.price_subtotal = subtotal_with_dis1
    #                     self.amount_amount1 = tax_amount
    #                     # self.amount_w_tax = subtotal_with_dis1 + tax_amount
    #                     dis2_amt = subtotal_with_dis1 * (self.discount3 / 100)
    #                     subtotal_with_dis2 = subtotal_with_dis1 - dis2_amt
    #                     # print("1st round of calculation")
    #                     self.price_subtotal = subtotal_with_dis2
    #                     self.amount_w_tax = subtotal_with_dis2 + tax_amount
    #                     self.grand_total = subtotal_with_dis2 + tax_amount
    #                     # print("price_subtotal", subtotal_with_dis2)
    #                     # print("total", subtotal_with_dis2 + tax_amount)
    #                     # print("extra dis", dis2_amt)
    #                     self.price_subtotal = self.amount_w_tax - self.amount_amount1
    #                     self.dis1 = discount1_amount
    #                     self.dis2 = dis2_amt
    #
    #
    #                 else:
    #                     discount1_amount = subtotal_wo_dis1 * (self.discount / 100)
    #                     item = self.invoice_line_tax_id4
    #                     subtotal_with_dis1 = subtotal_wo_dis1 - discount1_amount
    #                     tax_amount = subtotal_with_dis1 * (item / 100)
    #                     self.price_subtotal = subtotal_with_dis1
    #                     self.amount_amount1 = tax_amount
    #                     self.amount_w_tax = subtotal_with_dis1 + tax_amount
    #                     self.grand_total = subtotal_with_dis1 + tax_amount
    #                     self.dis1 = discount1_amount
    #             else:
    #                 item = self.invoice_line_tax_id4
    #                 tax_amount = subtotal_wo_dis1 * (item / 100)
    #                 self.amount_amount1 = tax_amount
    #                 self.amount_w_tax = subtotal_wo_dis1 + tax_amount
    #                 self.grand_total = subtotal_wo_dis1 + tax_amount
    #     if self.partner_id.supplier == True:
    #         self.rate_amt = self.amount_w_tax - self.amount_amount1
    #         # self.grand_total = self.amount_w_tax - self.amount_amount1
    #         # print("finallyyyyy", self.rate_amt)
    #
    # CUSTOMER EXTRA DISCOUNT

    @api.one
    @api.depends('product_id', 'medicine_name_subcat', 'medicine_grp', 'medicine_name_subcat', 'discount3',
                 'price_unit',
                 'quantity', 'amt_w_tax')
    def _compute_cus_ex_discount(self):
        for record in self:

            percentage = 0
            if record.partner_id.customer == True:
                print('record.rate_amtc',record.rate_amtc)
                if record.rate_amtc:
                    for rec in self:
                        # print("got")
                        new_rate = rec.rate_amtc
                        percentage = (new_rate / rec.price_subtotal) * 100
                        rec.new_disc = 100 - percentage

    medicine_rack = fields.Many2one('product.medicine.types', 'Rack')
    product_of = fields.Many2one('product.medicine.responsible', 'Company',default=lambda self: self._compute_default_target_field(),)

    @api.model
    def _compute_default_target_field(self):
        latest_entry_stock = self.env['entry.stock'].search([], order='id desc', limit=1)
        return latest_entry_stock.company.id if latest_entry_stock and latest_entry_stock.company else False


    medicine_name_subcat = fields.Many2one('product.medicine.subcat', 'Potency')
    medicine_name_packing = fields.Many2one('product.medicine.packing', 'Pack',default=lambda self: self._get_default_medicine_pack())

    # medicine_grp = fields.Many2one('product.medicine.group', 'GROUP',compute='_compute_taxes',readonly="0")
    medicine_grp = fields.Many2one('product.medicine.group', 'Grp', default=lambda self: self._get_default_medicine_group())

    # medicine_group = fields.Char('Group', related="product_id.medicine_group")
    batch = fields.Char("BATCH",)
    batch_2 = fields.Many2one('med.batch', "Batch", )
    # test = fields.Float('Test', compute="_get_sup_discount_amt")
    test = fields.Float('Test')
    # test2 = fields.Float('Test2',compute="_get_sup_discount2")
    test2 = fields.Float('Test2')
    test3 = fields.Float('Test3', compute="_compute_all")
    expiry_date = fields.Date(string='Exp')
    manf_date = fields.Date(string='Mfd')
    alert_date = fields.Date(string='Alert Date')
    avail_qty = fields.Float(string='Stock Total', related="product_id.qty_available")
    hsn_code = fields.Char('Hsn')
    # invoice_line_tax_id3 = fields.Many2one('tax.combo', string='Gst')
    invoice_line_tax_id4 = fields.Float(string='Tax')
    rack_qty = fields.Float(string="stock", compute='compute_stock_qty')
    rate_amt = fields.Float(string="Rate")
    rate_amtc = fields.Float(string="N-rate")
    dis1 = fields.Float('discount 1')
    dis2 = fields.Float('discount 2')
    grand_total = fields.Float('Grand Total')
    calc = fields.Float('Cal', compute="_compute_mass_discount", )
    calc2 = fields.Float('Cal2', )
    calc3 = fields.Float('Cal3', )
    new_disc = fields.Float('Dis2(%)', compute="_compute_cus_ex_discount", )
    amt_tax = fields.Float('Tax_amt', compute="_compute_customer_tax")
    amt_w_tax = fields.Float('Total', compute="_compute_customer_tax")
    doctor_name = fields.Many2one('res.partner', 'Doctor Name')
    doctor_name_1 = fields.Char('Doctor Name')
    address_new = fields.Text('Address')
    product_id = fields.Many2one('product.product', 'Medicine',domain=[('visible_in', '=', 'true')])

    price_subtotal = fields.Float(string='Amount', digits=dp.get_precision('Account'),
                                  store=True, readonly=True, compute='_compute_price', inverse='_inverse_compute_price')

    @api.model
    def _default_product_id(self):
        first_product = self.env['product.product'].search([('visible_in', '=', 'true')], limit=1)
        return first_product.id if first_product else False
    @api.model
    def _get_default_medicine_pack(self):
            name_pattern = '100ML'
            default_pack = self.env['account.invoice.line'].search([('medicine_name_packing', 'ilike', name_pattern)], limit=1)
            return default_pack.medicine_name_packing if default_pack else ''

    @api.model
    def _get_default_medicine_group(self):
        name_pattern = 'DIL'
        default_grp = self.env['account.invoice.line'].search([('medicine_grp', 'ilike', name_pattern)],
                                                               limit=1)
        return default_grp.medicine_grp if default_grp else ''

    @api.onchange('product_id', 'medicine_name_subcat', 'medicine_name_packing','product_of')
    def _onchange_fields(self):
        default_value = lambda self: self.env['product.medicine.group'].search([], limit=1).id
        for rec in self:
            if rec.invoice_id.type == 'out_invoice':
                if self.product_id and self.medicine_name_subcat and self.medicine_name_packing and self.product_of :
                    previous_line = self.env['account.invoice.line'].search([
                        ('product_id', '=', self.product_id.id),
                        ('medicine_name_subcat', '=', self.medicine_name_subcat.id),
                        ('medicine_name_packing', '=', self.medicine_name_packing.id),
                        ('product_of', '=', self.product_of.id)
                    ], limit=1, order='id desc')

                    if previous_line:

                        self.medicine_grp = previous_line.medicine_grp.id
                        self.product_id = previous_line.product_id.id
                        self.medicine_name_subcat = previous_line.medicine_name_subcat.id
                        self.medicine_name_packing = previous_line.medicine_name_packing.id
                        self.product_of = previous_line.product_of.id


                        self.write({
                            'medicine_grp': self.medicine_grp.id,
                            'product_id': self.product_id.id,
                            'medicine_name_subcat': self.medicine_name_subcat.id,
                            'medicine_name_packing': self.medicine_name_packing.id,
                            'product_of': self.product_of.id
                        })
                    else:
                        self._get_default_medicine_group()
                else:
                    self._get_default_medicine_group()

                # Update create_bool based on field presence
                self.create_bool = bool(self.product_id and self.medicine_name_subcat and self.medicine_name_packing and self.product_of)
        # @api.onchange('price_unit')
    # def _compute_manf_expiry_date_display(self):
    #     for record in self:
    #         if record.manf_date:
    #             # Compute/manipulate 'manf_date'
    #             manf_date_obj = datetime.datetime.strptime(record.manf_date, '%m/%Y')
    #             manf_date_str = manf_date_obj.strftime('%m/%Y')
    #             record.manf_date = manf_date_str
    #             record.manf_date_display = manf_date_str
    #         else:
    #             record.manf_date_display = ''
    #
    #         if record.expiry_date:
    #             # Compute/manipulate 'expiry_date'
    #             expiry_date_obj = datetime.datetime.strptime(record.expiry_date, '%m/%Y')
    #             expiry_date_str = expiry_date_obj.strftime('%m/%Y')
    #             record.expiry_date = expiry_date_str
    #             record.expiry_date_display = expiry_date_str
    #         else:
    #             record.expiry_date_display = ''

    def _inverse_compute_price(self):
        for rec in self:
            if rec.quantity * rec.price_unit > 0:
                discount_amount = (rec.quantity * rec.price_unit) - rec.price_subtotal
                percentage = (discount_amount * 100) / (rec.quantity * rec.price_unit)
                rec.discount = percentage
                rec.new_disc = percentage

    @api.onchange('price_subtotal')
    def onchange_price_subtotal(self):
        for rec in self:
            if rec.quantity * rec.price_unit > 0:
                discount_amount = (rec.quantity * rec.price_unit) - rec.price_subtotal
                percentage = (discount_amount * 100) / (rec.quantity * rec.price_unit)
                rec.discount = percentage
                rec.new_disc = percentage

    @api.onchange('product_id')
    def product_id_change_new(self):
        for rec in self:
            if rec.product_id:
                rec.name = rec.product_id.name
            # if rec.invoice_id:
            #     if rec.invoice_id.partner_id.supplier:
            #         self.search([('invoice_id', '=' , )])

    @api.onchange('medicine_grp')
    def medicine_grp_change_new(self):
        for rec in self:
            if rec.invoice_id.type == 'out_invoice':
                domain = []
                if rec.product_id:
                    domain += [('medicine_1', '=', rec.product_id.id)]
                # if rec.expiry_date:
                #     domain += [('expiry_date', '=', result.expiry_date)]
                if rec.product_of:
                    domain += [('company', '=', rec.product_of.id)]
                if rec.medicine_grp:
                    domain += [('medicine_grp1', '=', rec.medicine_grp.id)]
                if rec.medicine_name_packing:
                    domain += [('medicine_name_packing', '=', rec.medicine_name_packing.id)]
                if rec.medicine_name_subcat:
                    domain += [('potency', '=', rec.medicine_name_subcat.id)]
                rec.name = rec.product_id.name
                rack_ids = []
                stock = self.env['entry.stock'].search(domain)
                for rec in stock:
                    rack_ids.append(rec.rack.id)
                print("racks are", rack_ids)

                return {'domain': {'medicine_rack': [('id', '=', rack_ids)]}}

    @api.onchange('medicine_rack')
    def onchange_compute_stock_qty(self):
        for rec in self:
            if rec.invoice_id.type == 'out_invoice':
                if rec.medicine_rack:
                    domain = [('rack', '=', rec.medicine_rack.id)]
                    if rec.product_id:
                        domain += [('medicine_1', '=', rec.product_id.id)]
                    # if rec.expiry_date:
                    #     domain += [('expiry_date', '=', result.expiry_date)]
                    if rec.product_of:
                        domain += [('company', '=', rec.product_of.id)]
                    if rec.medicine_grp:
                        domain += [('medicine_grp1', '=', rec.medicine_grp.id)]
                    if rec.medicine_name_packing:
                        domain += [('medicine_name_packing', '=', rec.medicine_name_packing.id)]
                    if rec.medicine_name_subcat:
                        domain += [('potency', '=', rec.medicine_name_subcat.id)]
                    stock_ids = self.env['entry.stock'].search(domain)
                    rec.rack_qty = sum(stock_ids.mapped('qty'))

    @api.depends('medicine_rack')
    def compute_stock_qty(self):
        for rec in self:
            if rec.invoice_id.type == 'out_invoice':
                if rec.medicine_rack:
                    domain = [('rack', '=', rec.medicine_rack.id)]
                    if rec.product_id:
                        domain += [('medicine_1', '=', rec.product_id.id)]
                    # if rec.expiry_date:
                    #     domain += [('expiry_date', '=', result.expiry_date)]
                    if rec.product_of:
                        domain += [('company', '=', rec.product_of.id)]
                    if rec.medicine_grp:
                        domain += [('medicine_grp1', '=', rec.medicine_grp.id)]
                    if rec.medicine_name_packing:
                        domain += [('medicine_name_packing', '=', rec.medicine_name_packing.id)]
                    if rec.medicine_name_subcat:
                        domain += [('potency', '=', rec.medicine_name_subcat.id)]
                    stock_ids = self.env['entry.stock'].search(domain)
                    rec.rack_qty = sum(stock_ids.mapped('qty'))

    @api.onchange('medicine_name_subcat')
    def onchange_potency_id(self):
        for rec in self:
            if rec.product_of and rec.product_id:
                idss = set()
                medicine_grp = self.env['medpotency.combo'].search([('potency', '=', rec.medicine_name_subcat.id)])
                for grp in medicine_grp:
                    if not grp.medicine.id and not grp.company.id:
                        idss.add(grp.id)
                    if grp.medicine.id and not grp.company.id:
                        if grp.medicine.id == rec.product_id.id:
                            idss.add(grp.id)
                        else:
                            pass
                    if grp.medicine and grp.company:
                        if grp.medicine.id == rec.product_id.id and grp.company.id == rec.product_of.id:
                            idss.add(grp.id)
                        else:
                            pass
                medicine_grp_ids = self.env['product.medicine.group'].search(
                    [('potency_med_ids', '=', list(idss))])
                return {'domain': {'medicine_grp': [('id', 'in', medicine_grp_ids.ids)]}}

    @api.onchange('medicine_name_packing')
    def onchange_medicine_name_packing(self):
        for rec in self:
            if rec.product_of and rec.product_id and rec.medicine_name_subcat and rec.medicine_name_packing:
                domain = [('lists_id.supplier', '=', rec.invoice_id.partner_id.id),
                          ('potency', '=', rec.medicine_name_subcat.id),
                          ('company', '=', rec.product_of.id),
                          ('medicine_1', '=', rec.product_id.id),
                          ('medicine_name_packing', '=', rec.medicine_name_packing.id),
                          ]
                medicine_grp = self.env['list.discount'].search(domain, limit=1)
                if medicine_grp:
                    pass
                # else:
                #     raise Warning("This Combination not added in Supplier Discount")

    ###########    # tax selection-based on group and potency

    @api.onchange('medicine_grp','quantity','medicine_name_subcat')
    def onchange_group_id(self):
        for rec in self:
            if rec.medicine_grp.id:
                print('medicine group..............................................................................')
                # print("medicine group exist")
                # grp_obj = self.env['product.medicine.group'].search([('med_grp', '=', rec.medicine_grp.med_grp),
                #                                                     ])
                grp_obj = rec.medicine_grp
                if grp_obj:

                    grp_obj_line = grp_obj.potency_med_ids.search([('medicine', '=', rec.product_id.id),
                                                                   ('potency', '=', rec.medicine_name_subcat.id),
                                                                   ('company', '=', rec.product_of.id),
                                                                   ('groups_id', '=', grp_obj.id)
                                                                   ], order='id desc', limit=1)

                    if grp_obj_line:
                        if grp_obj_line.tax:
                            rec.invoice_line_tax_id4 = grp_obj_line.tax
                        else:
                            rec.invoice_line_tax_id4 = grp_obj.tax_rate

                        if grp_obj_line.hsn:
                            rec.hsn_code = grp_obj_line.hsn
                        else:
                            rec.hsn_code = grp_obj.hsn
                            # rec.hsn_code = grp_obj_line.hsn
                            # rec.invoice_line_tax_id4 = grp_obj_line.tax


                    else:
                        if rec.product_id.id and rec.medicine_name_subcat.id:
                            grp_obj_line = grp_obj.potency_med_ids.search([('medicine', '=', rec.product_id.id),
                                                                           (
                                                                           'potency', '=', rec.medicine_name_subcat.id),
                                                                           ('company', '=', None),
                                                                           ('groups_id', '=', grp_obj.id)
                                                                           ], order='id desc', limit=1)
                            if grp_obj_line:
                                if grp_obj_line.tax:
                                    rec.invoice_line_tax_id4 = grp_obj_line.tax
                                else:
                                    rec.invoice_line_tax_id4 = grp_obj.tax_rate

                                if grp_obj_line.hsn:
                                    rec.hsn_code = grp_obj_line.hsn
                                else:
                                    rec.hsn_code = grp_obj.hsn
                                    # rec.hsn_code = grp_obj_line.hsn
                                    # rec.invoice_line_tax_id4 = grp_obj_line.tax


                            else:
                                if rec.product_id.id and rec.product_of.id:
                                    grp_obj_line = grp_obj.potency_med_ids.search([('medicine', '=', rec.product_id.id),
                                                                                   ('potency', '=', None),
                                                                                   ('company', '=', rec.product_of.id),
                                                                                   ('groups_id', '=', grp_obj.id)
                                                                                   ], order='id desc', limit=1)
                                    if grp_obj_line:
                                        if grp_obj_line.tax:
                                            rec.invoice_line_tax_id4 = grp_obj_line.tax
                                        else:
                                            rec.invoice_line_tax_id4 = grp_obj.tax_rate

                                        if grp_obj_line.hsn:
                                            rec.hsn_code = grp_obj_line.hsn
                                        else:
                                            rec.hsn_code = grp_obj.hsn
                                            # rec.hsn_code = grp_obj_line.hsn
                                            # rec.invoice_line_tax_id4 = grp_obj_line.tax


                                    else:
                                        if rec.medicine_name_subcat.id and rec.product_of.id:
                                            grp_obj_line = grp_obj.potency_med_ids.search([('medicine', '=', None),
                                                                                           ('potency', '=',
                                                                                            rec.medicine_name_subcat.id),
                                                                                           ('company', '=',
                                                                                            rec.product_of.id),
                                                                                           (
                                                                                               'groups_id', '=',
                                                                                               grp_obj.id)
                                                                                           ], order='id desc', limit=1)
                                            if grp_obj_line:
                                                if grp_obj_line.tax:
                                                    rec.invoice_line_tax_id4 = grp_obj_line.tax
                                                else:
                                                    rec.invoice_line_tax_id4 = grp_obj.tax_rate

                                                if grp_obj_line.hsn:
                                                    rec.hsn_code = grp_obj_line.hsn
                                                else:
                                                    rec.hsn_code = grp_obj.hsn
                                                    # rec.hsn_code = grp_obj_line.hsn
                                                    # rec.invoice_line_tax_id4 = grp_obj_line.tax


                                            else:
                                                if rec.medicine_name_subcat.id:
                                                    grp_obj_line = grp_obj.potency_med_ids.search(
                                                        [('medicine', '=', None),
                                                         ('potency', '=', rec.medicine_name_subcat.id),
                                                         ('company', '=', None),
                                                         ('groups_id', '=', grp_obj.id)
                                                         ], order='id desc', limit=1)
                                                    if grp_obj_line:
                                                        if grp_obj_line.tax:
                                                            rec.invoice_line_tax_id4 = grp_obj_line.tax
                                                        else:
                                                            rec.invoice_line_tax_id4 = grp_obj.tax_rate

                                                        if grp_obj_line.hsn:
                                                            rec.hsn_code = grp_obj_line.hsn
                                                        else:
                                                            rec.hsn_code = grp_obj.hsn
                                                            # rec.hsn_code = grp_obj_line.hsn
                                                            # rec.invoice_line_tax_id4 = grp_obj_line.tax


                                                    else:
                                                        if rec.product_id.id:
                                                            grp_obj_line = grp_obj.potency_med_ids.search(
                                                                [('medicine', '=', rec.product_id.id),
                                                                 ('potency', '=', None),
                                                                 ('company', '=', None),
                                                                 ('groups_id', '=', grp_obj.id)
                                                                 ], order='id desc', limit=1)
                                                            if grp_obj_line:
                                                                if grp_obj_line.tax:
                                                                    rec.invoice_line_tax_id4 = grp_obj_line.tax
                                                                else:
                                                                    rec.invoice_line_tax_id4 = grp_obj.tax_rate

                                                                if grp_obj_line.hsn:
                                                                    rec.hsn_code = grp_obj_line.hsn
                                                                else:
                                                                    rec.hsn_code = grp_obj.hsn
                                                                    # rec.hsn_code = grp_obj_line.hsn
                                                                    # rec.invoice_line_tax_id4 = grp_obj_line.tax


                                                            else:
                                                                if rec.product_of.id:
                                                                    grp_obj_line = grp_obj.potency_med_ids.search(
                                                                        [('medicine', '=', None),
                                                                         ('potency', '=', None),
                                                                         ('company', '=', rec.product_of.id),
                                                                         ('groups_id', '=', grp_obj.id)
                                                                         ], order='id desc', limit=1)
                                                                    if grp_obj_line:

                                                                        if grp_obj_line.tax:
                                                                            rec.invoice_line_tax_id4 = grp_obj_line.tax
                                                                        else:
                                                                            rec.invoice_line_tax_id4 = grp_obj.tax_rate

                                                                        if grp_obj_line.hsn:
                                                                            rec.hsn_code = grp_obj_line.hsn
                                                                        else:
                                                                            rec.hsn_code = grp_obj.hsn
                                                                            # rec.hsn_code = grp_obj_line.hsn
                                                                            # rec.invoice_line_tax_id4 = grp_obj_line.tax

                                                                    else:
                                                                        rec.hsn_code = None
                                                                        rec.invoice_line_tax_id4 = 0
                                                                        raise Warning(
                                                                            "This Combination not added in Product Potency Group Linking")

                else:
                    rec.hsn_code = None
                    rec.invoice_line_tax_id4 = 0
                    raise Warning("This Combination not added in Product Potency Group Linking")
                if  rec.hsn_code == None:
                    raise Warning("HSN not Linked")

    # @api.onchange('medicine_grp')
    # def onchange_group_id(self):
    #     for rec in self:
    #         if self.medicine_grp.id:
    #             # print("medicine group exist")
    #             grp_obj = self.env['product.medicine.group'].search([])
    #             flag = 0
    #             for items in grp_obj:
    #                 # print("inside for loop")
    #                 for lines in items.potency_med_ids:
    #                     # print("1")
    #                     if (rec.product_id.id == lines.medicine.id):
    #                         # print("2")
    #
    #                         if (rec.medicine_name_subcat.id == lines.potency.id):
    #                             # print("3")
    #                             if (rec.product_of.id == lines.company.id):
    #                                 # print("4")
    #                                 rec.hsn_code = lines.hsn
    #                                 rec.invoice_line_tax_id4 = lines.tax
    #                                 rec.product_of = lines.company
    #                                 # print("print tax", lines.tax)
    #                                 flag = 1
    #             if flag == 1:
    #                 # print("flag is 0")
    #                 pass
    #             else:
    #                 grp_obj = self.env['tax.combo.new'].browse(rec.medicine_grp.id)
    #                 if grp_obj.hsn and grp_obj.tax_rate:
    #                     # print("exist both")
    #                     self.hsn_code = grp_obj.hsn
    #                     self.invoice_line_tax_id4 = grp_obj.tax_rate

    #################### PRODUCT SEARCH FOR INVOICE LINE

    @api.multi
    def _create_stock_moves(self, picking):
        moves = self.env['stock.move']
        done = self.env['stock.move'].browse()
        for line in self:
            price_unit = line.price_unit
            template = {
                'name': line.name or '',
                'product_id': line.product_id.id,
                'product_uom': line.product_id.uom_id.id,
                'location_id': line.invoice_id.partner_id.property_stock_supplier.id,
                'location_dest_id': picking.picking_type_id.default_location_dest_id.id,
                'picking_id': picking.id,
                'move_dest_id': False,
                'state': 'draft',
                'company_id': line.invoice_id.company_id.id,
                'price_unit': price_unit,
                'picking_type_id': picking.picking_type_id.id,
                'procurement_id': False,
                'route_ids': 1 and [
                    (6, 0, [x.id for x in self.env['stock.location.route'].search([('id', 'in', (2, 3))])])] or [],
                'warehouse_id': picking.picking_type_id.warehouse_id.id,
            }
            diff_quantity = line.quantity
            tmp = template.copy()
            tmp.update({
                'product_uom_qty': diff_quantity,
            })
            template['product_uom_qty'] = diff_quantity
            done += moves.create(template)
        return done

    def _create_stock_moves_transfer(self, picking):
        moves = self.env['stock.move']
        done = self.env['stock.move'].browse()
        for line in self:
            price_unit = line.price_unit
            template = {
                'name': line.name or '',
                'product_id': line.product_id.id,
                'product_uom': line.product_id.uom_id.id,
                'location_id': picking.picking_type_id.default_location_src_id.id,
                'location_dest_id': line.invoice_id.partner_id.property_stock_customer.id,
                'picking_id': picking.id,
                'move_dest_id': False,
                'state': 'draft',
                'company_id': line.invoice_id.company_id.id,
                'price_unit': price_unit,
                'picking_type_id': picking.picking_type_id.id,
                'procurement_id': False,
                'route_ids': 1 and [
                    (6, 0, [x.id for x in self.env['stock.location.route'].search([('id', 'in', (2, 3))])])] or [],
                'warehouse_id': picking.picking_type_id.warehouse_id.id,
            }
            diff_quantity = line.quantity
            tmp = template.copy()
            tmp.update({
                'product_uom_qty': diff_quantity,
            })
            template['product_uom_qty'] = diff_quantity
            done += moves.create(template)
        return done


class AccountInvoice(models.Model):
    _inherit = "account.invoice"
    _rec_name = "number2"
    _order = "number2 desc"

    @api.multi
    def open_password_wizard(self):
        """Opens the Password Wizard."""
        self.ensure_one()  # Ensure the method is called on a single record
        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoice Password Wizard',
            'res_model': 'invoice.password.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_invoice_id': self.id,
            },
        }
    @api.multi
    def open_supplier_password_wizard(self):
        """Opens the Password Wizard."""
        self.ensure_one()  # Ensure the method is called on a single record
        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoice Password Wizard',
            'res_model': 'supplier.password.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_invoice_id': self.id,
            },
        }
    @api.multi
    def open_wizard_action(self):
        return ({
            'type': 'ir.actions.act_window',
            'name': 'Invoice Wizard',
            'res_model': 'customer.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'current',
            'context': {
                'default_invoice_id': self.id,
                'default_partner_id': self.partner_id.id,
                'invoice_id': self.id,
                'active_model': self._name,
            },
        } )

    @api.multi
    def open_wizard_action_sup(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoice Wizard',
            'res_model': 'supplier.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'current',
            'context': {
                'default_invoice_id': self.id,
                'default_partner_id': self.partner_id.id,
                'invoice_id': self.id,
                'active_model': self._name,
            },
        }

    validated_by_user = fields.Char(string="Validated By", readonly=True,store=True)
    packing_invoice = fields.Boolean("Packing Slip?")
    hold_invoice = fields.Boolean("Holding Invoice?")
    cus_invoice = fields.Boolean("Customer Invoice?")
    quotation_invoice = fields.Boolean("quotation Invoice?")
    invoice_color_class = fields.Boolean('Invoice Color Class')
    hold_invoice_id = fields.Many2one("account.invoice",
                                      domain=[('type', '=', 'out_invoice'), ('hold_invoice', '=', True)])
    partner_id = fields.Many2one('res.partner',create=True)
    cus_inv_number = fields.Char()
    advance_amount = fields.Float('Advance Amount',compute='get_advance_amount', store=True)
    cus_invoice_id = fields.Many2one("account.invoice",
                                     domain=[('type', '=', 'out_invoice'), ('cus_invoice', '=', True)])
    pack_open_cus_invoice_id = fields.Many2one("account.invoice",
                                               domain=[('type', '=', 'out_invoice'), ('cus_invoice', '=', True)])
    pack_invoice_id = fields.Many2one("account.invoice",
                                      domain=[('type', '=', 'out_invoice'), ('packing_invoice', '=', True)])
    bill_discount = fields.Float("Bill Discount")
    gst_type = fields.Selection([
        ('gst_minus', 'GST MINUS'),
        ('gst_plus', 'GST PLUS')],default='gst_minus')
    account_id = fields.Many2one('account.account', string='Account', required = False, default=13)
    date_invoices = fields.Date(default=fields.Date.today(),readonly=True,string="Invoice Date")
    hold_invoice_link = fields.Char(string="Invoice Link", compute='_compute_invoice_link', readonly=True)

    # action_invoice_tree_id = fields.Many2one('ir.actions.act_window', compute='_compute_action_id',
    #                                          string="Invoice Tree Action")
    # @api.depends('action_invoice_tree_id')
    # def _compute_action_id(self):
    #     for record in self:
    #         action = self.env.ref('pharmacy_mgmnt.action_holding_invoice', raise_if_not_found=False)
    #         if action:
    #             record.action_invoice_tree_id = action.id



    @api.constrains('pay_mode', 'partner_id')
    @api.onchange('pay_mode', 'partner_id')
    def _check_credit_eligibility(self):
        for rec in self:
            if rec.pay_mode == 'credit' and not rec.partner_id.limit_amt:
                raise ValidationError(_('Customer not eligible for credit payment'))
            if rec.pay_mode == 'cash' and  rec.partner_id.limit_amt:
                rec.invoice_color_class= True
                print ('haiiiiiiiiiiiiiiiiiiiii.................................')



    #
    # @api.onchange('partner_id','pay_mode')
    # def _compute_invoice_color(self):
    #     for invoice in self:
    #
    #         if invoice.partner_id.limit_amt and invoice.pay_mode == 'cash':
    #                 invoice.invoice_color_class=True
    #                 print('condition satisfied.................................................')
    #         else:
    #             invoice.invoice_color_class = False
    #             print ('not satisfied......................................................')
    #             invoice.invoice_color_class = ''


    @api.depends('partner_id')
    def get_advance_amount(self):
        for rec in self:
            if rec.advance_amount == 0:
                rec.advance_amount = rec.partner_id.advance_amount

    @api.depends('hold_invoice_link')
    def _compute_invoice_link(self):
        for record in self:
            invoice_url = "http://0.0.0.0:8069/web#page=0&limit=80&view_type=list&model=account.invoice&action={}".format(
                self.env.ref('pharmacy_mgmnt.action_holding_invoice', raise_if_not_found=False).id)
            record.hold_invoice_link = invoice_url
    @api.model
    def default_get(self, fields):
        res = super(AccountInvoice, self).default_get(fields)
        if res.get('type') == 'out_invoice':
            res.update({'partner_id': 23})
        return res

    @api.onchange("bill_discount")
    def onchange_bill_discount(self):
        if self.partner_id.supplier:
            for rec in self.invoice_line:
                rec.discount2 = self.bill_discount
            self.invoice_line._compute_all()
        else:
            pass

    # @api.onchange("bill_discount")
    # def onchange_bill_discount(self):
    #     for rec in self.invoice_line:
    #         if not rec.discount2:
    #             rec.discount2 = self.bill_discount
    #             rec.discount3 += self.bill_discount
    #         else:
    #             rec.discount3 -= rec.discount2
    #             rec.discount2 = self.bill_discount
    #             rec.discount3 += self.bill_discount
    @api.multi
    def previous_invoice(self):
        next_inv = self.env['account.invoice'].search(
            [(('id', '=', self.id - 1))])
        print(next_inv, 'next_inv')
        if next_inv:
            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            redirect_url = "%s/web#id=%d&view_type=form&model=account.invoice&menu_id=331&action=400" % (
                base_url, next_inv)
            return {
                'type': 'ir.actions.act_url',
                'url': redirect_url,
                'target': 'self',
            }
            # return {
            #     'view_mode': 'form',
            #     'res_id': self.id - 1,
            #     'res_model': 'account.invoice',
            #     'view_id': self.env.ref('account.invoice_form').id,
            #     'type': 'ir.actions.act_window',
            #     'context': {'type': 'out_invoice'},
            #     'target': 'current',
            #     'clear': 1,
            # }
        else:
            raise Warning("Create a new record")

    @api.multi
    def next_invoice(self):
        next_inv = self.env['account.invoice'].search(
            [(('id', '=', self.id + 1))])
        if next_inv:
            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            redirect_url = "%s/web#id=%d&view_type=form&model=account.invoice&menu_id=331&action=400" % (
                base_url, next_inv)
            return {
                'type': 'ir.actions.act_url',
                'url': redirect_url,
                'target': 'self',
            }
            # return {
            #     'view_mode': 'form',
            #     'res_id': self.id + 1,
            #     'res_model': 'account.invoice',
            #     'view_id': self.env.ref('account.invoice_form').id,
            #     'type': 'ir.actions.act_window',
            #     'context': {'type': 'out_invoice'},
            #     'target': 'current',
            #     'clear': 1,
            # }
        else:
            raise Warning("Create a new record")

    @api.multi
    def open_supplier_invoice(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        redirect_url = "%s/web#id=%d&view_type=form&model=account.invoice&menu_id=328&action=399" % (
            base_url, self.invoices_id.id)
        print(redirect_url, '.......>')
        return {
            'type': 'ir.actions.act_url',
            'url': redirect_url,
            'target': 'self',
        }

    @api.multi
    def open_customer_invoice(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        redirect_url = "%s/web#id=%d&view_type=form&model=account.invoice&menu_id=331&action=400" % (
            base_url, self.cus_invoice_id.id)
        return {
            'type': 'ir.actions.act_url',
            'url': redirect_url,
            'target': 'self',
        }

    @api.multi
    def onchange_cus_invoice_id(self):
        if self.cus_invoice_id:
            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            redirect_url = "%s/web#id=%d&view_type=form&model=account.invoice&menu_id=331&action=400" % (
                base_url, self.cus_invoice_id.id)
            print(redirect_url, 'customer........>')
            return {
                'type': 'ir.actions.act_url',
                'url': redirect_url,
                'target': 'self',
            }
        else:
            pass
        # return {
        #     'view_mode': 'form',
        #     'res_id': self.cus_invoice_id.id,
        #     'res_model': 'account.invoice',
        #     'view_id': self.env.ref('account.invoice_form').id,
        #     'type': 'ir.actions.act_window',
        #     'context': {'type': 'out_invoice'},
        #     'target': 'current',
        #     'clear': 1,
        # }

    @api.multi
    def onchange_pack_cus_invoice_id(self):
        if self.pack_open_cus_invoice_id:
            # hold = self.env['account.invoice'].search([('id','=',self.hold_invoice_id.id),('hold_invoice','=',True),('type','=','out_invoice')])
            # print(hold.hold_invoice,"hold")
            # print(hold.id,"hold.id")
            # print(self.hold_invoice_id.id,"self.hold_invoice_id")
            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            redirect_url = "%s/web#id=%d&view_type=form&model=account.invoice&menu_id=331&action=400" % (
                base_url, self.pack_open_cus_invoice_id.id)
            print(redirect_url, 'packing........>')
            return {
                'type': 'ir.actions.act_url',
                'url': redirect_url,
                'target': 'self',
            }
        else:
            pass

    @api.multi
    def onchange_hold_invoice_id(self):
        if self.hold_invoice_id:
            # hold = self.env['account.invoice'].search([('id','=',self.hold_invoice_id.id),('hold_invoice','=',True),('type','=','out_invoice')])
            # print(hold.hold_invoice,"hold")
            # print(hold.id,"hold.id")
            # print(self.hold_invoice_id.id,"self.hold_invoice_id")
            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            redirect_url = "%s/web#id=%d&view_type=form&model=account.invoice&menu_id=347&action=408" % (
                base_url, self.hold_invoice_id.id)
            return {
                'type': 'ir.actions.act_url',
                'url': redirect_url,
                'target': 'self',
            }
            # return {
            #     'name': _('Holding Invoice'),  # Title of the wizard
            #     'view_mode': 'form',  # Display the wizard in form view
            #     'res_id': self.hold_invoice_id.id,  # ID of the created wizard record
            #     'res_model': 'account.invoice',  # Model of the wizard
            #     'type': 'ir.actions.act_window',
            #     'target': 'self',  # Open the wizard in a new window or tab
            # }
        else:
            pass

    @api.multi
    def onchange_packing_invoice_id(self):
        if self.pack_invoice_id:
            # hold = self.env['account.invoice'].search([('id','=',self.hold_invoice_id.id),('hold_invoice','=',True),('type','=','out_invoice')])
            # print(hold.hold_invoice,"hold")
            # print(hold.id,"hold.id")
            # print(self.hold_invoice_id.id,"self.hold_invoice_id")
            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            redirect_url = "%s/web#id=%d&view_type=form&model=account.invoice&menu_id=348&action=409" % (
                base_url, self.pack_invoice_id.id)
            return {
                'type': 'ir.actions.act_url',
                'url': redirect_url,
                'target': 'self',
            }
            # return {
            #     'name': _('Holding Invoice'),  # Title of the wizard
            #     'view_mode': 'form',  # Display the wizard in form view
            #     'res_id': self.hold_invoice_id.id,  # ID of the created wizard record
            #     'res_model': 'account.invoice',  # Model of the wizard
            #     'type': 'ir.actions.act_window',
            #     'target': 'self',  # Open the wizard in a new window or tab
            # }
        else:
            pass

    @api.onchange('financial_year')
    def onchange_pay_mode(self):
        self.date_invoice = date.today()
        if self.type == 'out_invoice' and self.cus_invoice == True:
            res1 = self.env['account.invoice'].search(
                [('type', '=', 'out_invoice'), ('cus_invoice', '=', True)], limit=1)
            number = self.env['ir.sequence'].get('customer.account.invoice')
            self.number2 = number
            self.cus_inv_number = number
            self.seq = 1
            if res1:
                # last_index = int(res1.number2.split('/')[1]) + 1
                # self.number2 = res1.number2.split('/')[0] + "/" + str(last_index).zfill(4)
                # self.cus_inv_number = res1.number2.split('/')[0] + "/" + str(last_index).zfill(4)
                # self.seq = res1.seq + 1
                last_index = int(res1.number2.split('/')[0]) + 1
                print(last_index, 'last_index', res1)
                self.number2 = str(last_index).zfill(4) + "/" + res1.number2.split('/')[1]
                self.cus_inv_number = str(last_index).zfill(4) + "/" + res1.number2.split('/')[1]
                self.seq = res1.seq + 1
            else:
                pass
        if self.type == 'out_invoice' and self.hold_invoice == True:
            res1 = self.env['account.invoice'].search(
                [('type', '=', 'out_invoice'), ('hold_invoice', '=', True)], limit=1)
            number = self.env['ir.sequence'].get('holding.invoice')
            self.number2 = number
            self.cus_inv_number = number
            self.seq = 1
            if res1:
                last_index = int(res1.number2.split('/')[0]) + 1
                print(last_index, 'last_index', res1)
                self.number2 = str(last_index).zfill(4) + "/" + res1.number2.split('/')[1]
                self.cus_inv_number = str(last_index).zfill(4) + "/" + res1.number2.split('/')[1]
                self.seq = res1.seq + 1
            else:
                pass
        if self.type == 'out_invoice' and self.packing_invoice == True:
            res1 = self.env['account.invoice'].search(
                [('type', '=', 'out_invoice'), ('packing_invoice', '=', True)], limit=1)
            number = self.env['ir.sequence'].get('packing.slip.invoice')
            self.number2 = number
            self.cus_inv_number = number
            self.seq = 1
            if res1:
                last_index = int(res1.number2.split('/')[0]) + 1
                print(last_index, 'last_index', res1)
                self.number2 = str(last_index).zfill(4) + "/" + res1.number2.split('/')[1]
                self.cus_inv_number = str(last_index).zfill(4) + "/" + res1.number2.split('/')[1]
                self.seq = res1.seq + 1
            else:
                pass
        if self.type == 'in_invoice':
            res1 = self.env['account.invoice'].search(
                [('type', '=', 'in_invoice')], limit=1)
            number = self.env['ir.sequence'].get('supplier.account.invoice')
            self.number2 = number
            self.seq = 1
            if res1:
                last_index = int(res1.number2.split('/')[0]) + 1
                self.number2 = str(last_index).zfill(4) + "/" + res1.number2.split('/')[1]
                self.cus_inv_number = str(last_index).zfill(4) + "/" + res1.number2.split('/')[1]
                self.seq = res1.seq + 1
            else:
                pass
        # self.number2 = self.env['ir.sequence'].next_by_code('customer.account.invoice')
        # if self.type == 'out_invoice':
        #     self.partner_id = self.env['res.partner'].search(['|', ('id', '=', 24), ('customer', '=', True)],
        #                                                      limit=1).id
        # else:
        #     pass

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(AccountInvoice, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar,
                                                          submenu=submenu)
        if view_type == 'form':
            set_invoice_line_readonly = self.env.context.get('set_invoice_line_readonly')
            if set_invoice_line_readonly:
                doc = etree.XML(res['arch'])
                for node in doc.xpath("//field[@name='invoice_line']"):
                    modifiers = json.loads(node.get("modifiers", "{}"))
                    modifiers['readonly'] = True
                    node.set("modifiers", json.dumps(modifiers))
                res['arch'] = etree.tostring(doc, encoding='unicode')
        return res

    @api.multi
    def name_get(self):
        TYPES = {
            'out_invoice': _('Invoice'),
            'in_invoice': _('Supplier Invoice'),
            'out_refund': _('Refund'),
            'in_refund': _('Supplier Refund'),
        }
        result = []
        for inv in self:
            result.append((inv.id, "%s %s" % (TYPES[inv.type], inv.number2 or inv.name or '')))
        return result

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        recs = self.browse()
        if name:
            recs = self.search([('number', '=', name)] + args, limit=limit)
        if not recs:
            recs = self.search([('number2', '=', name)] + args, limit=limit)
        if not recs:
            recs = self.search([('name', operator, name)] + args, limit=limit)
        return recs.name_get()

    search_items = fields.Char('.')

    invoices_id = fields.Many2one('account.invoice', 'Select Previous Invoice')
    period_id = fields.Many2one('account.period', 'Select Period')

    @api.multi
    def load(self):
        # inv_obj = self.env['account.invoice'].browse(['|',('id', '=', self.invoices_id.id),('type', '=', "in_invoice")])
        new_lines = []  # Moved the new_lines list outside of the loop
        if self.invoices_id:
            for line in self.invoices_id.invoice_line:
                new_lines.append([0, 0, {
                    'name': line.name,
                    'product_id': line.product_id.id,
                    'medicine_name_subcat': line.medicine_name_subcat.id,
                    'medicine_name_packing': line.medicine_name_packing.id,
                    'product_of': line.product_of.id,
                    'medicine_grp': line.medicine_grp.id,
                    'batch_2': line.batch_2.id,
                    'hsn_code': line.hsn_code,
                    'quantity': line.quantity,
                    'price_unit': line.price_unit,
                    'discount': line.discount,
                    'price_subtotal': line.price_subtotal,
                    'invoice_line_tax_id4': line.invoice_line_tax_id4,
                    'amount_amount1': line.amount_amount1,
                    'amount_w_tax': line.amount_w_tax,
                    'manf_date': line.manf_date,
                    'expiry_date': line.expiry_date,
                    'medicine_rack': line.medicine_rack.id,
                }])
        self.invoice_line = new_lines

    state = fields.Selection([
        ('draft', 'Draft'),
        ('packing_slip', 'Packing Slips'),
        ('holding_invoice', 'Holding Invoice'),
        ('proforma', 'Pro-forma'),
        ('proforma2', 'Pro-forma'),
        ('open', 'Open'),
        ('paid', 'Paid'),
        ('cancel', 'Cancelled'),
        ('done', 'Received'),

    ], string='Status', index=True, readonly=True, default='draft',
        track_visibility='onchange', copy=False,
        help=" * The 'Draft' status is used when a user is encoding a new and unconfirmed Invoice.\n"
             " * The 'Pro-forma' when invoice is in Pro-forma status,invoice does not have an invoice number.\n"
             " * The 'Open' status is used when user create invoice,a invoice number is generated.Its in open status till user does not pay invoice.\n"
             " * The 'Paid' status is set automatically when the invoice is paid. Its related journal entries may or may not be reconciled.\n"
             " * The 'Cancelled' status is used when user cancel invoice.")

    @api.one
    def add_items(self):
        pass

    number2 = fields.Char()
    # number2 = fields.Char(
    #     'Inv Number', size=16, copy=False,
    #     readonly=True, store=True,
    #     default=lambda self:
    #     self.env['ir.sequence'].next_by_code('customer.account.invoice'))
    duplicate = fields.Boolean()
    seq = fields.Integer()
    holding_invoice = fields.Boolean()  # NOT WORKING IN SOME CONDITION USE holding_invoice
    packing_slip = fields.Boolean()  # NOT WORKING IN SOME CONDITION  USE packing_slip
    packing_slip_new = fields.Boolean()  # NOT WORKING IN SOME CONDITION

    @api.multi
    def invoice_print(self):
        if self.type == 'out_invoice':
            if self.state == 'open':
                self.state = 'paid'
            if self.state == 'draft':
                self.action_date_assign()
                self.action_move_create()
                self.action_number()
                # self.invoice_validate()
        return super(AccountInvoice, self).invoice_print()

    @api.multi
    def print_e_way_report(self):
        datas = {
            'ids': self._ids,
            'model': self._name,
            'form': self.read(),
            'context': self._context,
        }
        data = self.env['ir.actions.report.xml'].search(
            [('model', '=', 'account.invoice'), ('report_name', '=', 'pharmacy_mgmnt.e_way_cus_report_template',)])
        data.download_filename = 'E-way report.pdf'
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'pharmacy_mgmnt.e_way_cus_report_template',
            'file': 'filename',
            'datas': datas,
            'report_type': 'qweb-pdf',
        }

    @api.multi
    def move_to_holding_invoice(self):
        for record in self:
            res = self.env['account.invoice'].search(
                [('type', '=', 'out_invoice'), ('hold_invoice', '=', True)], limit=1)
            if res:
                last_index = int(res.number2.split('/')[0]) + 1
                record.number2 = str(last_index).zfill(4) + "/" + res.number2.split('/')[1]
                record.cus_inv_number = str(last_index).zfill(4) + "/" + res.number2.split('/')[1]
                record.seq = res.seq + 1
                record.packing_invoice = False
                record.hold_invoice = True
                record.cus_invoice = False
                record.state = "draft"
            else:
                last_index = 1
                current_year = datetime.datetime.now().year
                record.number2 = str(last_index).zfill(4) + "/" + str(current_year)
                record.cus_inv_number = str(last_index).zfill(4) + "/" + str(current_year)
                record.seq = 1
                record.packing_invoice = False
                record.hold_invoice = True
                record.cus_invoice = False
                record.state = "draft"
        return {
            'type': 'ir.actions.client',
            'tag': 'history_back',
        }

        # return {
        #     'name': _('Customer Invoices'),
        #     'view_type': 'tree',
        #     'view_mode': 'tree',
        #     'view_id': self.env.ref('account.invoice_tree').id,
        #     'res_model': 'account.invoice',
        #     'context': "{'type':'out_invoice'}",
        #     'type': 'ir.actions.act_window',
        #     'target': 'main',
        # }

    # @api.multi
    # def move_to_holding_invoice(self):
    #     for record in self:
    #         # if record.state == 'packing_slip':
    #         #     record.state = 'open'
    #         # else:
    #         record.state = 'holding_invoice'
    #         record.holding_invoice = False
    #         record.number2 = self.env['ir.sequence'].next_by_code('holding.invoice')
    #     return

    # @api.multi
    # def move_to_picking_slip(self):
    #     for record in self:
    #         if record.invoice_line:
    #             record.action_stock_transfer()
    #         record.packing_slip = True
    #         record.packing_slip_new = True
    #         # record.action_date_assign()
    #         # record.action_move_create()
    #         # record.action_number()
    #         # record.invoice_validate()
    #         record.state = 'packing_slip'
    #
    #         record.number2 = self.env['ir.sequence'].next_by_code('packing.slip.invoice')
    #
    #     return

    # @api.multi
    # def move_to_picking_slip(self):
    #     for record in self:
    #         # if record.state == 'packing_slip':
    #         #     record.state = 'open'
    #         # else:
    #         record.state = 'packing_slip'
    #         record.packing_slip = False
    #         record.packing_slip_new = False
    #         record.number2 = self.env['ir.sequence'].next_by_code('packing.slip.invoice')
    #     return

    # @api.multi
    # def import_to_invoice(self):
    #     # for record in self:
    #     #     for line in record.invoice_line:
    #     #         domain = [('medicine_1','=',line.product_id.name),
    #     #             ('potency','=',line.medicine_name_subcat.id),
    #     #             ('medicine_name_packing','=',line.medicine_name_packing.id),
    #     #             ('company','=',line.product_of.id),
    #     #             ('medicine_grp1','=',line.medicine_grp.id),
    #     #             ('mrp','=',line.price_unit),
    #     #             ('manf_date','=',line.manf_date),
    #     #             ('expiry_date','=',line.expiry_date),
    #     #             ('rack','=',line.medicine_rack.id),
    #     #             ('hsn_code','=',line.hsn_code)]
    #     #         stock = self.env['entry.stock'].search(domain)
    #     #         stock.qty_received -= line.quantity
    #     #         if stock.qty_received < 0:
    #     #             stock.qty_received = 0
    #     for record in self:
    #         res = self.env['account.invoice'].search(
    #             [('type', '=', 'out_invoice'), ('cus_invoice', '=', True)], limit=1)
    #         last_index = int(res.number2.split('/')[0]) + 1
    #         record.number2 = str(last_index).zfill(4) + "/" + res.number2.split('/')[1]
    #         record.cus_inv_number = str(last_index).zfill(4) + "/" + res.number2.split('/')[1]
    #         record.seq = res.seq + 1
    #         record.packing_invoice = False
    #         record.hold_invoice = False
    #         record.cus_invoice = True
    #         record.state = "draft"
    #     base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
    #     invoice_id = self.id
    #     redirect_url = "%s/web#id=%d&view_type=form&model=account.invoice&menu_id=331&action=400" % (
    #         base_url, invoice_id)
    #     return {
    #         'type': 'ir.actions.act_url',
    #         'url': redirect_url,
    #         'target': 'self',
    #     }
    @api.multi
    def import_to_invoice(self):
        for record in self:
            # Search for the latest customer invoice
            res = self.env['account.invoice'].search(
                [('type', '=', 'out_invoice'), ('cus_invoice', '=', True)], limit=1)
            last_index = int(res.number2.split('/')[0]) + 1
            new_invoice_number = str(last_index).zfill(4) + "/" + res.number2.split('/')[1]

            # Update the current record with new customer invoice details
            record.number2 = new_invoice_number
            record.cus_inv_number = new_invoice_number
            record.seq = res.seq + 1
            record.packing_invoice = False
            record.hold_invoice = False
            record.cus_invoice = True
            record.state = "draft"

            # Update or create the related packing slip entry with the same invoice number
            packing_slip = self.env['account.invoice'].search( [('type', '=', 'out_invoice'), ('packing_invoice', '=', True)], limit=1)
            if  packing_slip:
                self.env['account.invoice'].create({
                    'invoice_id':self.id,
                    'invoice_number': new_invoice_number,
                    'state': 'draft',

                })
            else:
                packing_slip.write({
                    'invoice_number': new_invoice_number,
                    'state': 'draft',
                })


        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        invoice_id = self.id
        redirect_url = "%s/web#id=%d&view_type=form&model=account.invoice&menu_id=331&action=400" % (
            base_url, invoice_id)
        return {
            'type': 'ir.actions.act_url',
            'url': redirect_url,
            'target': 'self',
        }

    @api.multi
    def invoice_open(self):
        self.ensure_one()
        # Search for record belonging to the current staff
        record = self.env['hiworth.invoice'].search([('origin', '=', self.name)])

        context = self._context.copy()
        context['type2'] = 'out'
        # context['default_name'] = self.id
        if record:
            res_id = record[0].id
        else:
            res_id = False
        # Return action to open the form view
        return {
            'name': 'Invoice view',
            'view_type': 'form',
            'view_mode': 'form',
            'views': [(False, 'form')],
            'res_model': 'hiworth.invoice',
            'view_id': 'hiworth_invoice_form',
            'type': 'ir.actions.act_window',
            'res_id': res_id,
            'context': context,
        }

    @api.onchange('invoice_line', 'invoice_line.quantity', 'invoice_line.price_unit', 'invoice_line.discount',
                  'invoice_line.price_subtotal', 'invoice_line.invoice_line_tax_id4')
    def onchange_credit_limit_checking(self):
        for rec in self:
            if rec.partner_id.customer:
                if rec.pay_mode == 'credit':
                    credit_amount = rec.partner_id.limit_amt
                    used = rec.partner_id.used_credit_amt
                    bal = credit_amount - used
                    if (bal <= 0) or (bal < rec.amount_total):
                        raise except_orm(_('Credit Limit Exceeded!'), ('This Customers Credit Limit Amou'
                                                                       'nt Rs. ' + str(
                            credit_amount) + '  has been Crossed.' + "\n" 'Check  ' + rec.partner_id.name + 's' + ' Credit Limits'))

                    if (rec.partner_id.credit_end_date < self.date_invoice):
                        raise except_orm(_('CREDIT DAYS LIMIT REACHED!'), (
                                'This Customers Credit Limit Days Are Ended' + "\n" 'Please Update the Customer Form'))

    # @api.constrains('create_id', 'password')
    # def check_password(self):
    #     for record in self:
    #         if record.create_id.rec_password == record.password:
    #             # record.create_bool = True
    #             pass
    #         else:
    #             # record.create_bool = False
    #             raise ValidationError("Enter the correct password")

    @api.constrains('invoice_line')
    def check_invoice_line(self):
        for record in self:
            if record.invoice_line:
                record.create_bool = True
            else:
                record.create_bool = False

    # MY CODE........................................
    @api.model
    def create(self, vals):
        # previous_invoice_number = self.env['account.invoice'].search([], order='seq desc', limit=1).number2.split('/')
        invoice_type = self.env.context.get('default_type') or self._context.get('default_type')
        packing_slip = self.env.context.get('default_packing_invoice') or self._context.get('default_packing_invoice')
        holding_invoice = self.env.context.get('default_hold_invoice') or self._context.get('default_hold_invoice')
        cus_invoice = self.env.context.get('default_cus_invoice') or self._context.get('default_cus_invoice')

        if invoice_type == 'in_invoice':
            res4 = self.env['account.invoice'].search([('type', '=', 'in_invoice')], limit=1)
            number = self.env['ir.sequence'].get('supplier.account.invoice')
            vals['number2'] = number
            vals['cus_inv_number'] = number
            vals['seq'] = 1
            if res4:
                last_index = int(res4.number2.split('/')[0]) + 1
                vals['number2'] = str(last_index).zfill(4) + "/" + res4.number2.split('/')[1]
                vals['cus_inv_number'] = str(last_index).zfill(4) + "/" + res4.number2.split('/')[1]
                vals['seq'] = res4.seq + 1
            else:
                pass
        if invoice_type == 'out_invoice' and cus_invoice == True:
            res1 = self.env['account.invoice'].search(
                [('type', '=', 'out_invoice'), ('cus_invoice', '=', True)], limit=1)
            number = self.env['ir.sequence'].get('customer.account.invoice')
            vals['number2'] = number
            # print(vals['number2'],'number')
            vals['cus_inv_number'] = number
            vals['seq'] = 1
            if res1:
                last_index = int(res1.number2.split('/')[0]) + 1
                print(last_index, 'last_index', res1)
                vals['number2'] = str(last_index).zfill(4) + "/" + res1.number2.split('/')[1]
                vals['cus_inv_number'] = str(last_index).zfill(4) + "/" + res1.number2.split('/')[1]
                vals['seq'] = res1.seq + 1
            else:
                pass
        if packing_slip == True and invoice_type == 'out_invoice':
            res2 = self.env['account.invoice'].search(
                [('type', '=', 'out_invoice'), ('packing_invoice', '=', True), ('hold_invoice', '=', False), ], limit=1)
            number = self.env['ir.sequence'].get('packing.slip.invoice')
            vals['number2'] = number
            vals['cus_inv_number'] = number
            vals['seq'] = 1
            if res2:
                last_index = int(res2.number2.split('/')[0]) + 1
                vals['number2'] = str(last_index).zfill(4) + "/" + res2.number2.split('/')[1]
                vals['cus_inv_number'] = str(last_index).zfill(4) + "/" + res2.number2.split('/')[1]
                vals['seq'] = res2.seq + 1
            else:
                pass
        if holding_invoice == True and invoice_type == 'out_invoice':
            res3 = self.env['account.invoice'].search(
                [('type', '=', 'out_invoice'), ('hold_invoice', '=', True), ('packing_invoice', '=', False)], limit=1)
            number = self.env['ir.sequence'].get('holding.invoice')
            vals['number2'] = number
            vals['cus_inv_number'] = number
            vals['seq'] = 1
            if res3:
                last_index = int(res3.number2.split('/')[0]) + 1
                print(last_index, 'last_index', res3)
                vals['number2'] = str(last_index).zfill(4) + "/" + res3.number2.split('/')[1]
                vals['cus_inv_number'] = str(last_index).zfill(4) + "/" + res3.number2.split('/')[1]
                vals['seq'] = res3.seq + 1
            else:
                pass
        result = super(AccountInvoice, self).create(vals)
        return result

    #     # ................. OLD CODE..............
    #     # if 'duplicate' in self._context:
    #     #     if self._context['duplicate']:
    #     #         vals.update({'number2': self.browse(self._context['inv_id']).number2, 'duplicate': True})
    #
    #     # result = super(AccountInvoice, self).create(vals)
    #     # if result.type == 'in_invoice' and not result.number2:
    #     #     result.number2 = self.env['ir.sequence'].next_by_code('supplier.account.invoice')
    #     #
    #     # if result.type == 'out_invoice' and not result.number2 and not result.packing_slip and not result.holding_invoice:
    #     #     result.number2 = self.env['ir.sequence'].next_by_code('customer.account.invoice')
    #     #
    #     # if result.packing_slip:
    #     #     result.number2 = self.env['ir.sequence'].next_by_code('packing.slip.invoice')
    #     #     result.state = 'packing_slip'
    #     #     result.packing_slip_new = True
    #     #
    #     # if result.holding_invoice:
    #     #     result.number2 = self.env['ir.sequence'].next_by_code('holding.invoice')
    #     #     result.holding_invoice = True
    #     #     result.state = 'holding_invoice'
    #     # return result
    # endofmycode.............................................
    # updated code................................................
    # @api.model
    # def create(self, vals):
    #     invoice_type = self.env.context.get('default_type') or self._context.get('default_type')
    #     packing_slip = self.env.context.get('default_packing_invoice') or self._context.get('default_packing_invoice')
    #     holding_invoice = self.env.context.get('default_hold_invoice') or self._context.get('default_hold_invoice')
    #     cus_invoice = self.env.context.get('default_cus_invoice') or self._context.get('default_cus_invoice')
    #
    #     res = None
    #     number = False
    #
    #     if invoice_type == 'in_invoice':
    #         res = self.env['account.invoice'].search([('type', '=', 'in_invoice')], order='number2 desc', limit=1)
    #         number = self.env['ir.sequence'].get('supplier.account.invoice')
    #     elif cus_invoice:
    #         cus_res = self.env['account.invoice'].search(
    #             [('cus_invoice', '=', True), ('number2', '!=', None)], order='number2 desc', limit=1)
    #         number = self.env['ir.sequence'].get('customer.account.invoice')
    #     elif packing_slip:
    #         res = self.env['account.invoice'].search(
    #             [('type', '=', 'out_invoice'), ('packing_invoice', '=', True)], order='number2 desc', limit=1)
    #         number = self.env['ir.sequence'].get('packing.slip.invoice')
    #     elif holding_invoice:
    #         res = self.env['account.invoice'].search(
    #             [('type', '=', 'out_invoice'), ('hold_invoice', '=', True), ('packing_invoice', '=', False)],
    #             order='number2 desc', limit=1)
    #         number = self.env['ir.sequence'].get('holding.invoice')
    #
    #     if res and res.number2:
    #         last_index = int(res.number2.split('/')[-1])
    #         vals['number2'] = res.number2.split('/')[0] + '/' + str(last_index + 1)
    #         vals['seq'] = res.seq + 1
    #     elif cus_invoice and cus_res and cus_res.number2:
    #         last_index = int(cus_res.number2.split('/')[-1])
    #         vals['number2'] = cus_res.number2.split('/')[0] + '/' + str(last_index + 1)
    #         vals['seq'] = cus_res.seq + 1
    #     else:
    #         vals['number2'] = number
    #         vals['seq'] = 1
    #
    #     result = super(AccountInvoice, self).create(vals)
    #
    #     if cus_invoice and cus_res and cus_res.number2:
    #         next_number = int(cus_res.number2.split('/')[-1]) + 1
    #         sequence = self.env['ir.sequence'].sudo().search([('code', '=', 'customer.account.invoice')], limit=1)
    #         sequence.number_next_actual = next_number
    #
    #     if 'sequence' in locals() and 'next_number' in locals():
    #         sequence.sudo().write({'number_next_actual': next_number})
    #
    #     return result

    # @api.model
    # def create(self, vals):
    #     previous_invoice = self.env['account.invoice'].search([], order='seq desc', limit=1)
    #     previous_invoice_number = previous_invoice.number2.split(
    #         '/') if previous_invoice and previous_invoice.number2 else None
    #     invoice_type = self.env.context.get('default_type') or self._context.get('default_type')
    #     packing_slip = self.env.context.get('default_packing_invoice') or self._context.get('default_packing_invoice')
    #     holding_invoice = self.env.context.get('default_hold_invoice') or self._context.get('default_hold_invoice')
    #     cus_invoice = self.env.context.get('default_cus_invoice') or self._context.get('default_cus_invoice')
    #
    #     res = None  # Default value for 'res'
    #     number = False  # Default value for 'number'
    #
    #     if invoice_type == 'in_invoice':
    #         res = self.env['account.invoice'].search([('type', '=', 'in_invoice')], limit=1)
    #         number = self.env['ir.sequence'].get('supplier.account.invoice')
    #     elif cus_invoice == True:
    #         cus_res = self.env['account.invoice'].search(
    #             [('cus_invoice', '=', True), ('number2', '!=', None)], limit=1)
    #         number = self.env['ir.sequence'].get('customer.account.invoice')
    #         print("number........................", number)
    #         print("number2........................", cus_res.number2)
    #     elif packing_slip == True:
    #         res = self.env['account.invoice'].search(
    #             [('type', '=', 'out_invoice'), ('packing_invoice', '=', True)], limit=1)
    #         number = self.env['ir.sequence'].get('packing.slip.invoice')
    #         print("res packing", res)
    #     elif holding_invoice == True:
    #         print("packing invoice", )
    #         print("packing", packing_slip)
    #         print("holding", holding_invoice)
    #         res = self.env['account.invoice'].search(
    #             [('type', '=', 'out_invoice'), ('hold_invoice', '=', True), ('packing_invoice', '=', False)], limit=1)
    #         print("res holding", res)
    #         number = self.env['ir.sequence'].get('holding.invoice')
    #
    #     if previous_invoice_number is None:
    #         vals['number2'] = number
    #         vals['seq'] = 1
    #     else:
    #         if cus_invoice == True:
    #             if not cus_res:
    #                 vals['number2'] = number
    #                 vals['seq'] = 1
    #             else:
    #                 last_index = int(cus_res.number2.split('/')[-1])
    #                 vals['number2'] = cus_res.number2.split('/')[0] + "/" + str(last_index+1)
    #                 vals['seq'] = cus_res.seq + 1
    #         elif invoice_type == 'in_invoice':
    #             last_index = int(res.number2.split('/')[-1]) + 1
    #             vals['number2'] = res.number2.split('/')[0] + "/" + str(last_index)
    #             vals['seq'] = res.seq + 1
    #         elif packing_slip == True:
    #             vals['number2'] = number
    #             vals['seq'] = 1
    #         elif holding_invoice == True:
    #             if not res:
    #                 vals['number2'] = number
    #                 vals['seq'] = 1
    #             else:
    #                 last_index = int(res.number2.split('/')[-1]) + 1
    #                 vals['number2'] = res.number2.split('/')[0] + "/" + str(last_index)
    #                 vals['seq'] = res.seq + 1
    #
    #     result = super(AccountInvoice, self).create(vals)
    #     return result
    #

    # end...................................................
    #
    @api.multi
    def write(self, vals):
        if 'internal_number' in vals:
            vals['internal_number'] = self.number2
            vals['name'] = self.number2
        return super(AccountInvoice, self).write(vals)

    @api.multi
    def unlink(self):
        for record in self:
            if record.state not in ['draft', 'holding_invoice', 'packing_slip']:
                raise Warning("Only Draft Invoice can be deleted")
            else:
                if record.invoice_line:
                    for rec in record.invoice_line:
                        same_ids = self.env['entry.stock'].search([('invoice_line_id', '=', rec.id_for_ref)],limit=1)
                        if same_ids:
                            same_ids.qty += rec.quantity
                        else:
                            pass
                else:
                    pass
        return super(AccountInvoice, self).unlink()

    def copy(self, cr, uid, id, default=None, context=None):
        context.update({'duplicate': True, 'inv_id': id})
        result = super(AccountInvoice, self).copy(cr, uid, id, default, context)
        return result

    @api.multi
    def action_discount1(self):
        return {
            'name': 'group discount',
            'view_type': 'form',
            'view_mode': 'tree',
            'domain': [('inv_id', '=', self.id)],
            'res_model': 'group.discount.copy',
            'type': 'ir.actions.act_window',
            'context': {'current_id': self.id},

        }

    @api.multi
    def action_discount(self):
        if not self.invoice_line:
            prev_rec = self.env['group.discount'].search([])
            if prev_rec:
                for rec in prev_rec:
                    rec.unlink()

        return {
            'name': 'group discount',
            'view_type': 'form',
            'view_mode': 'form,tree',
            'target': 'new',
            'res_model': 'group.discount',
            'type': 'ir.actions.act_window',
            'context': {'current_id': self.id},

        }

    #     if self.pay_mode == 'credit':
    #         if self.partner_id.customer:
    #             print("inside credits onchange")

    def get_year(self):
        year = self.env['account.fiscalyear'].search([('state', '=', 'draft')],limit=1,order="id desc")
        print(year, 'yearyear')
        if year:
            return year

    local_customer = fields.Boolean("Local Customer", default=True)
    interstate_customer = fields.Boolean("Interstate Customer")
    b2b = fields.Boolean("B2B")
    b2c = fields.Boolean("B2C", default=True)
    bill_nature = fields.Selection([('gst', 'GST'), ('igst', 'IGST')], default='gst', compute='compute_bill')
    doctor_name = fields.Many2one('res.partner', 'Doctor Name')
    doctor_name_1 = fields.Many2one('res.partner', 'Doctor')

    res_person = fields.Many2one('res.partner', string="Responsible Person")
    address_new = fields.Text('Address', related="partner_id.address_new")
    financial_year = fields.Many2one('account.fiscalyear', 'Financial Year', default=get_year)
    inv_sup_no = fields.Char('Invoice No')
    inv_amount = fields.Float('Invoice Amount')

    @api.depends('interstate_customer', 'local_customer')
    def compute_bill(self):
        for rec in self:
            if rec.local_customer:
                rec.bill_nature = 'gst'
            if rec.interstate_customer:
                rec.bill_nature = 'igst'

    @api.multi
    def tree_stock(self):
        rec = self.env['entry.stock'].sudo.search([])
        return {
            'name': 'stock tree',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'entry.stock',
            'type': 'ir.actions.act_window',

            'search_view_id': self.env.ref('pharmacy_mgmnt.stock_search_view').id
        }

    @api.multi
    def wiz_tree(self):
        rec = self.env['entry.stock'].sudo.search([])
        return {
            'context': self.env.context,
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'entry.stock',
            'res_id': self.id,
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

    def invoice_pay_customer(self, cr, uid, ids, context=None):
        if not ids: return []
        dummy, view_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'account_voucher',
                                                                             'view_vendor_receipt_dialog_form')

        inv = self.browse(cr, uid, ids[0], context=context)
        inv.write({'validated_by': inv.validated_by_user})
        # if inv.type == "out_invoice":
        #     inv.residual += inv.amount_discount + inv.amount_tax
        return {
            'name': _("Pay Invoice"),
            'view_mode': 'form',
            'view_id': view_id,
            'view_type': 'form',
            'res_model': 'account.voucher',
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'new',
            'domain': '[]',
            'context': {
                'payment_expected_currency': inv.currency_id.id,
                'default_partner_id': self.pool.get('res.partner')._find_accounting_partner(inv.partner_id).id,
                'default_amount': inv.type in ('out_refund', 'in_refund') and -inv.residual or inv.residual,
                'default_reference': inv.name,
                'default_name': inv.name,
                'close_after_process': True,
                'invoice_type': inv.type,
                'invoice_id': inv.id,
                'default_pay_mode': inv.pay_mode,
                'default_res_person': inv.res_person.id,
                'default_validated_by': inv.validated_by_user,
                'default_type': inv.type in ('out_invoice', 'out_refund') and 'receipt' or 'payment',
                'type': inv.type in ('out_invoice', 'out_refund') and 'receipt' or 'payment'
            }
        }

    @api.onchange('residual')
    def onchange_residual(self):
        if self.residual <= 0.00:
            if self.state == 'open':
                self.state = 'paid'
                self.update({'state': 'paid'})
        else:
            print("not working")

    # @api.onchange('residual')
    # def onchange_residual(self):
    #     if self.residual == 0.00:
    #         print('yes')
    #         if self.state == 'open':
    #             print("working...........................................................")
    #             self.state = 'paid'
    #             self.write({'state': 'paid'})
    #     else:
    #         print("not working")

    # FOOTER TOTAL AMT CALCULATIONS

    discount_category = fields.Many2one('cus.discount', 'Discount Category', related='partner_id.discount_category')
    discount_type = fields.Selection([('percent', 'Percentage'), ('amount', 'Amount'), ], default='percent',
                                     string='Discount Type', readonly=True,
                                     states={'draft': [('readonly', False)]}, )
    discount_rate = fields.Float('Discount Rate',
                                 digits_compute=dp.get_precision('Account'),
                                 readonly=True,
                                 states={'draft': [('readonly', False)]}, )
    amount_discount = fields.Float(string='Discount',
                                   digits=dp.get_precision('Account'),
                                   readonly=True, compute='_compute_amount', store=True)
    amount_untaxed = fields.Float(string='Subtotal', digits=dp.get_precision('Account'),
                                  readonly=True, compute='_compute_amount', track_visibility='always')
    amount_tax = fields.Float(string='Tax', digits=dp.get_precision('Account'),
                              readonly=True, compute='_compute_amount', store=True)
    amount_total = fields.Float(string='Total', digits=dp.get_precision('Account'),
                                readonly=True, compute='_compute_amount')
    amount_tax_custom = fields.Float(string='Tax', digits=dp.get_precision('Account'),
                                     store=True, readonly=True, compute='_compute_amount')
    # amount_tax_custom = fields.Float(string='Tax', digits=dp.get_precision('Account'),
    #     store=True, readonly=True, compute='_compute_amount_tax')

    cus_title_1 = fields.Many2one('customer.title', "Customer Type", related="partner_id.cus_title")
    cust_area = fields.Many2one('customer.area', "Customer Area", related="partner_id.cust_area")
    create_id = fields.Many2one('res.users', "Created By", Required=True)
    password = fields.Char(Required=True, )
    create_bool = fields.Boolean(Default=False)
    paid_bool = fields.Boolean('Invoice Paid?')
    pay_mode = fields.Selection([('cash', 'Cash'),('upi', 'UPI'),('card','Card'),('credit', 'Credit'),('cheque','Cheque')], 'Payment Mode',
                                default='cash')
    amount_in_words = fields.Char('Amount in Words', compute='_compute_amount_in_words')
    phone_number = fields.Char('Phone No',size=10,related="partner_id.mobile")

    @api.onchange('phone_number')
    def onchange_phone_number(self):
        if self.phone_number:
            partner_id = self.env['res.partner'].search([('mobile', '=', self.phone_number)], limit=1)
            if partner_id and  self.partner_id != partner_id.id:
                self.partner_id = partner_id.id
            else:
                return {
                    'warning': {
                        'title': _('Warning'),
                        'message': _('Check the number. No partner found with this phone number.'),
                    },
                }


    @api.depends('amount_total')
    def _compute_amount_in_words(self):
        for invoice in self:
            invoice.amount_in_words = num2words(invoice.amount_total, lang='en').title()

    @api.depends('amount_total')
    def _compute_amount_tax(self):
        for rec in self:
            rec.amount_tax_custom = rec.amount_total - (rec.amount_untaxed - rec.amount_discount)
            rec.amount_tax = rec.amount_tax_custom

    @api.one
    @api.depends('invoice_line.price_subtotal', 'tax_line.amount')
    def _compute_amount(self):
        total_tax_sup = 0.0
        if self.partner_id.supplier:
            amount_untaxed = sum(self.invoice_line.mapped('rate_amt'))
            amount_total_w_tax = sum(self.invoice_line.mapped('amount_w_tax'))
            if amount_total_w_tax <= 0:
                amount_total_w_tax = sum(self.invoice_line.mapped('grand_total'))
            total_price_amount = sum(self.invoice_line.mapped(lambda l: l.quantity * l.price_unit))
            # total_tax_amount = sum(self.invoice_line.mapped('amount_amount1'))
            # total_discount = sum(self.invoice_line.mapped(lambda l: l.dis1 + l.dis2))
            total_tax_amount = amount_total_w_tax - amount_untaxed
            total_discount = total_price_amount - amount_untaxed
            # self.rate_amt = self.amount_w_tax - self.amount_amount1
            # discount_2 = 0.0
            # for lines in self.invoice_line:
            #     discount_2 += (lines.quantity * lines.price_unit) * lines.discount3 / 100
            # discount_2 += (lines.quantity * lines.price_unit) * lines.discount3 / 100
            self.amount_untaxed = total_price_amount
            self.amount_tax = total_tax_amount
            self.amount_tax_custom = total_tax_amount
            self.amount_discount = total_discount
            self.amount_total = round(amount_total_w_tax)

        if self.partner_id.customer:
            # print(amount_untaxed,'first')
            amount_untaxed = sum(self.invoice_line.mapped('price_subtotal'))
            amount_total_w_tax = sum(self.invoice_line.mapped('amt_w_tax'))
            if amount_total_w_tax <= 0:
                amount_total_w_tax = sum(self.invoice_line.mapped('grand_total'))
            total_products_tax = sum(self.invoice_line.mapped('product_tax'))
            total_price_amount = sum(self.invoice_line.mapped(lambda l: l.quantity * l.price_unit))
            # total_tax_amount = sum(self.invoice_line.mapped('amt_tax'))
            # total_discount = sum(self.invoice_line.mapped(lambda l: l.dis1 + l.dis2))
            total_tax_amount = abs(amount_total_w_tax - amount_untaxed)
            total_discount = total_price_amount - amount_untaxed
            self.amount_untaxed = total_price_amount
            self.amount_tax = total_products_tax
            self.amount_tax_custom = total_products_tax
            self.amount_discount = total_discount
            # if self.advance_amount:
            #     amount_total_w_tax -= self.advance_amount
            # else:
            #     pass
            if self.advance_amount:
                if self.advance_amount > amount_total_w_tax:
                    if self.advance_amount == amount_total_w_tax:
                        # self.advance_amount = 0
                        amount_total_w_tax = 0
                    else:
                        # self.advance_amount -= amount_total_w_tax
                        amount_total_w_tax = 0
                else:
                    amount_total_w_tax -= self.advance_amount
                    # self.advance_amount = 0
            self.amount_total = round(amount_total_w_tax)
            self.amount_residual = round(amount_total_w_tax)

    # @api.one
    # @api.depends('invoice_line.price_subtotal', 'tax_line.amount')
    # def _compute_amount(self):
    #     if self.partner_id.supplier == True:
    #         disc = 0.0
    #         total_dis = 0
    #         tax_total = 0
    #         test = 0
    #         test2 =0
    #         test3 =0
    #         for inv in self:
    #             for line in inv.invoice_line:
    #                 print (line.discount)
    #                 disc += (line.quantity * line.price_unit) * line.discount / 100
    #                 test += line.grand_total
    #                 test3 = test3+line.rate_amt
    #                 test2 = test2+(line.quantity * line.price_unit)
    #                 # test2 = test2+line.rate_amt
    #                 total_dis = total_dis +(line.dis1 + line.dis2)
    #                 tax_total = tax_total+line.amount_amount1
    #         self.amount_untaxed = test2
    #         self.amount_tax = tax_total
    #         self.amount_tax_custom = tax_total
    #         total_d = test2 - test3
    #         self.amount_discount = total_d
    #         # self.amount_total = ((test2 -total_d) + tax_total)
    #         self.amount_total = round(test)
    #     if self.partner_id.customer == True:
    #         disc = 0.0
    #         total_dis = 0
    #         tax_total = 0
    #         test = 0
    #         test2 = 0
    #         test3 = 0
    #         for inv in self:
    #             for line in inv.invoice_line:
    #                 print (line.discount)
    #                 disc += (line.quantity * line.price_unit) * line.discount / 100
    #                 test += line.amt_w_tax
    #                 test3 = test3 + line.amt_w_tax
    #                 test2 = test2 + (line.quantity * line.price_unit)
    #                 total_dis = total_dis + (line.dis1 + line.dis2)
    #                 tax_total = tax_total + line.amt_tax
    #         self.amount_untaxed = test2
    #         self.amount_tax = tax_total
    #         total_d = test2 - (test3-tax_total)
    #         self.amount_discount = total_d
    #         # self.amount_total = ((test2 -total_d) + tax_total)
    #         self.amount_total = round(test)

    @api.onchange('discount_category')
    def onchange_category_id(self):
        for rec in self:
            if rec.type != 'in_invoice':
                rec.discount_rate = rec.discount_category.percentage
                for line in rec.invoice_line:
                    line.discount = rec.discount_category.percentage

    @api.depends('discount_category')
    def compute_discount_rate(self):
        for rec in self:
            if rec.type != 'in_invoice':
                rec.discount_rate = rec.discount_category.percentage

    @api.multi
    def compute_discount(self, discount):
        for inv in self:
            val1 = val2 = 0.0
            disc_amnt = 0.0
            val2 = sum(line.amount for line in self.tax_line)
            for line in inv.invoice_line:
                val1 += (line.quantity * line.price_unit)
                line.discount = discount
                disc_amnt += (line.quantity * line.price_unit) * discount / 100
            total = val1 + val2 - disc_amnt
            self.amount_discount = disc_amnt
            # self.amount_tax = val2
            self.amount_total = total

    @api.onchange('discount_type', 'discount_rate')
    def supply_rate(self):
        for inv in self:
            if inv.discount_rate != 0:
                for line in self.invoice_line:
                    line.test3 = inv.discount_rate
                amount = sum(line.price_subtotal for line in self.invoice_line)
                tax = sum(line.amount for line in self.tax_line)
                if inv.discount_type == 'percent':
                    self.compute_discount(inv.discount_rate)
                else:
                    total = 0.0
                    discount = 0.0
                    for line in inv.invoice_line:
                        total += (line.quantity * line.price_unit)
                    if inv.discount_rate != 0:
                        discount = (inv.discount_rate / total) * 100
                    self.compute_discount(discount)

    @api.model
    def _prepare_refund(self, invoice, date=None, period_id=None, description=None, journal_id=None):
        res = super(AccountInvoice, self)._prepare_refund(invoice, date, period_id,
                                                          description, journal_id)
        res.update({
            'discount_type': self.discount_type,
            'discount_rate': self.discount_rate,
        })
        return res

    # UPDATE TAX BUTTON

    @api.multi
    def button_reset_taxes(self):
        res = super(AccountInvoice, self).button_reset_taxes()
        # add custom codes here
        tax_total = 0
        for lines in self.invoice_line:
            if lines.amount_amount1:
                tax_total = tax_total + lines.amount_amount1
        self.amount_tax = tax_total
        self.amount_total = self.amount_total + tax_total
        return res

    ####################### BALANCE CALCULATION###########################################

    def _compute_residual(self):
        for rec in self:
            rec.residual = 0.0
            # Each partial reconciliation is considered only once for each invoice it appears into,
            # and its residual amount is divided by this number of invoices
            partial_reconciliations_done = []
            for line in rec.sudo().move_id.line_id:
                if line.account_id.type not in ('receivable', 'payable'):
                    continue
                if line.reconcile_partial_id and line.reconcile_partial_id.id in partial_reconciliations_done:
                    continue
                # Get the correct line residual amount
                if line.currency_id == rec.currency_id:
                    line_amount = line.amount_residual_currency if line.currency_id else line.amount_residual
                else:
                    from_currency = line.company_id.currency_id.with_context(date=line.date)
                    line_amount = from_currency.compute(line.amount_residual, rec.currency_id)
                # For partially reconciled lines, split the residual amount
                if line.reconcile_partial_id:
                    partial_reconciliation_invoices = set()
                    for pline in line.reconcile_partial_id.line_partial_ids:
                        if pline.invoice and rec.type == pline.invoice.type:
                            partial_reconciliation_invoices.update([pline.invoice.id])
                    line_amount = rec.currency_id.round(line_amount / len(partial_reconciliation_invoices))
                    partial_reconciliations_done.append(line.reconcile_partial_id.id)
                rec.residual += line_amount
            rec.residual = round(max(rec.residual, 0.0))
                # if record.type == "out_invoice" and record.residual != 0:
                #     record.residual += round(record.amount_tax)
                #     record.residual = max(record.residual, 0.0)
                # else:
                #     record.residual = max(record.residual, 0.0)
            if rec.state == 'paid':
                rec.residual = 0.0

    # def _compute_residual(self):
    #     for record in self:
    #         record.residual = 0.0
    #         partial_reconciliations_done = []
    #         for line in record.sudo().move_id.line_id:
    #             if line.account_id.type not in ('receivable', 'payable'):
    #                 continue
    #             if line.reconcile_partial_id and line.reconcile_partial_id.id in partial_reconciliations_done:
    #                 continue
    #             if line.currency_id == record.currency_id:
    #                 line_amount = line.amount_residual_currency - line.tax_amount if line.currency_id else line.amount_residual - line.tax_amount
    #             else:
    #                 from_currency = line.company_id.currency_id.with_context(date=line.date)
    #                 line_amount = from_currency.compute(line.amount_residual - line.tax_amount, record.currency_id)
    #             if line.reconcile_partial_id:
    #                 partial_reconciliation_invoices = set()
    #                 for pline in line.reconcile_partial_id.line_partial_ids:
    #                     if pline.invoice and record.type == pline.invoice.type:
    #                         partial_reconciliation_invoices.update([pline.invoice.id])
    #                 line_amount = record.currency_id.round(line_amount / len(partial_reconciliation_invoices))
    #                 partial_reconciliations_done.append(line.reconcile_partial_id.id)
    #             record.residual += line_amount
    #         record.residual = max(record.residual, 0.0)
    #         if record.state == 'paid':
    #             record.residual = 0.0

    ########################## INVOICE STOCK MOVE ##############################

    @api.model
    def _default_picking_receive(self):
        type_obj = self.env['stock.picking.type']
        company_id = self.env.context.get('company_id') or self.env.user.company_id.id
        types = type_obj.search([('code', '=', 'incoming'), ('warehouse_id.company_id', '=', company_id)], limit=1)
        if not types:
            types = type_obj.search([('code', '=', 'incoming'), ('warehouse_id', '=', False)])
        return types[:1]

    @api.model
    def _default_picking_transfer(self):
        type_obj = self.env['stock.picking.type']
        company_id = self.env.context.get('company_id') or self.env.user.company_id.id
        types = type_obj.search([('code', '=', 'outgoing'), ('warehouse_id.company_id', '=', company_id)], limit=1)
        if not types:
            types = type_obj.search([('code', '=', 'outgoing'), ('warehouse_id', '=', False)])
        return types[:4]

    picking_count = fields.Integer(string="Count")
    invoice_picking_id = fields.Many2one('stock.picking', string="Picking Id")
    picking_type_id = fields.Many2one('stock.picking.type', 'Picking Type', required=True,
                                      default=_default_picking_receive,
                                      help="This will determine picking type of incoming shipment")
    picking_transfer_id = fields.Many2one('stock.picking.type', 'Deliver To', required=True,
                                          default=_default_picking_transfer,
                                          help="This will determine picking type of outgoing shipment")

    @api.multi
    def action_stock_receive(self):
        for line in self.invoice_line:
            self.env['stock.pick'].create({
                'partner_id': self.partner_id.id,
                'product_id': line.product_id.id,
                'product_uom_qty': line.quantity,
                'date': self.date_invoice,
                'date_exp': line.expiry_date})

        for order in self:
            if not order.invoice_line:
                pass
                # raise UserError(_('Please create some invoice lines.'))
            if not self.number:
                pass
                # raise UserError(_('Please Validate invoice.'))
            if not self.invoice_picking_id:
                pick = {
                    'picking_type_id': self.picking_type_id.id,
                    'partner_id': self.partner_id.id,
                    'origin': self.number,
                    'location_dest_id': self.picking_type_id.default_location_dest_id.id,
                    'location_id': self.partner_id.property_stock_supplier.id
                }
                picking = self.env['stock.picking'].create(pick)
                self.invoice_picking_id = picking.id
                self.picking_count = len(picking)
                moves = order.invoice_line.filtered(
                    lambda r: r.product_id.type in ['product', 'consu'])._create_stock_moves(picking)
                move_ids = moves.action_confirm()
                move_ids = moves.action_assign()
                move_ids = moves.action_done()

    # @api.multi
    # def action_stock_transfer(self):
    #     if not self.packing_slip_new:
    #         for line in self.invoice_line:
    #             if not line.stock_transfer_id:
    #                 stock_transfer_id = self.env['stock.transfer'].create({
    #                     'partner_id': self.partner_id.id,
    #                     'title': self.cus_title_1.id,
    #                     'product_id': line.product_id.id,
    #                     'product_uom_qty': line.quantity,
    #                     'date': self.date_invoice})
    #                 line.stock_transfer_id = stock_transfer_id.id
    #
    #                 domain = [('qty', '>=', line.quantity)]
    #                 if line.product_id:
    #                     domain += [('medicine_1', '=', line.product_id.id)]
    #                 if line.expiry_date:
    #                     domain += [('expiry_date', '=', line.expiry_date)]
    #                 if line.medicine_rack:
    #                     domain += [('rack', '=', line.medicine_rack.id)]
    #                 if line.product_of:
    #                     domain += [('company', '=', line.product_of.id)]
    #                 if line.medicine_grp:
    #                     domain += [('medicine_grp1', '=', line.medicine_grp.id)]
    #                 if line.medicine_name_packing:
    #                     domain += [('medicine_name_packing', '=', line.medicine_name_packing.id)]
    #                 if line.medicine_name_subcat:
    #                     domain += [('potency', '=', line.medicine_name_subcat.id)]
    #
    #                 entry_stock_ids = self.env['entry.stock'].search(domain, order='id asc')
    #                 if sum(entry_stock_ids.mapped('qty')) <= 0 or not entry_stock_ids:
    #                     if line.medicine_rack:
    #                         domain.remove(('rack', '=', line.medicine_rack.id))
    #                     if line.expiry_date:
    #                         domain.remove(('expiry_date', '=', line.expiry_date))
    #                     entry_stock_ids = self.env['entry.stock'].search(domain, order='id asc')
    #                 if not entry_stock_ids:
    #                     domain.remove(('qty', '>=', line.quantity))
    #                     domain += [('qty', '>=', 0)]
    #                     entry_stock_ids = self.env['entry.stock'].search(domain, order='id asc')
    #
    #                 # if not entry_stock_ids or sum(entry_stock_ids.mapped('qty')) <= 0:
    #                 #     raise Warning(
    #                 #         _('Only we have %s Products with current combination in stock') % str(
    #                 #             int(line.stock_entry_qty) + int(sum(entry_stock_ids.mapped('qty')))))
    #
    #                 quantity = line.quantity
    #                 for stock in entry_stock_ids:
    #                     # if quantity > 0:
    #                     if stock.qty >= quantity:
    #                         stock.write({
    #                             'qty': stock.qty - quantity,
    #                         })
    #                         break
    #                     else:
    #                         quantity -= stock.qty
    #                         stock.write({
    #                             'qty': 0,
    #                         })
    #
    #                 line.stock_entry_qty = line.quantity
    #
    #         for order in self:
    #             if not order.invoice_line:
    #                 pass
    #                 # raise UserError(_('Please create some invoice lines.'))
    #             if not self.number:
    #                 pass
    #                 # raise UserError(_('Please Validate invoice.'))
    #             if not self.invoice_picking_id:
    #                 pick = {
    #                     'picking_type_id': self.picking_transfer_id.id,
    #                     'partner_id': self.partner_id.id,
    #                     'origin': self.number,
    #                     'location_dest_id': self.partner_id.property_stock_customer.id,
    #                     'location_id': self.picking_transfer_id.default_location_src_id.id
    #                 }
    #                 picking = self.env['stock.picking'].create(pick)
    #                 self.invoice_picking_id = picking.id
    #                 self.picking_count = len(picking)
    #                 moves = order.invoice_line.filtered(
    #                     lambda r: r.product_id.type in ['product', 'consu'])._create_stock_moves_transfer(picking)
    #                 move_ids = moves.action_confirm()
    #                 move_ids = moves.action_assign()
    #                 move_ids = moves.action_done()

    @api.multi
    def action_view_picking(self):
        action = self.env.ref('stock.action_picking_tree_ready')
        result = action.read()[0]
        result.pop('id', None)
        result['context'] = {}
        result['domain'] = [('id', '=', self.invoice_picking_id.id)]
        pick_ids = sum([self.invoice_picking_id.id])
        if pick_ids:
            res = self.env.ref('stock.view_picking_form', False)
            result['views'] = [(res and res.id or False, 'form')]
            result['res_id'] = pick_ids or False
        return result

    @api.multi
    def invoice_validate(self):
        # if self.type != 'in_invoice' and not self.packing_slip:
        #     self.action_stock_transfer()
        # if self.type == 'in_invoice':
        #     for result in self.invoice_line:
        #     # if result.invoice_id.type == 'in_invoice' and result.quantity != 0:
        #         vals = {
        #             'supplier_id': self.partner_id.id,
        #             'expiry_date': result.expiry_date,
        #             'manf_date': result.manf_date,
        #             'company': result.product_of.id,
        #             'medicine_1': result.product_id.id,
        #             'potency': result.medicine_name_subcat.id,
        #             'medicine_name_packing': result.medicine_name_packing.id,
        #             'medicine_grp1': result.medicine_grp.id,
        #             'batch_2': result.batch_2.id,
        #             'mrp': result.price_unit,
        #             'qty': result.quantity,
        #             'rack': result.medicine_rack.id,
        #             'hsn_code': result.hsn_code,
        #             'discount': result.discount,
        #             'invoice_line_tax_id4': result.invoice_line_tax_id4,
        #             'stock_date': date.today(),
        #         }
        #         stock_entry = self.env['entry.stock'].create(vals)
        #         result.stock_entry_id = stock_entry.id
        return self.write({'state': 'open'})

    @api.multi
    def delete_line(self):
        for rec in self:
            if rec.invoice_line:
                for res in rec.invoice_line:
                    if res.delete_bool == True:
                        data = self.env['entry.stock'].search([('invoice_line_id', '=', res.id_for_ref)])
                        if data:
                            data.qty += res.quantity
                            data.write({'qty': data.qty})
                        res.unlink()
                    elif not res.product_id or not res.medicine_name_subcat or not res.medicine_grp or not res.price_unit or not res.quantity:
                        res.unlink()
                    else:
                        pass
            else:
                raise ValidationError("No invoice Lines")


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    is_quotation = fields.Boolean('Is Quotation')