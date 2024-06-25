from datetime import datetime

from dateutil.relativedelta import relativedelta

from openerp import models, fields, api
from openerp.exceptions import MissingError


class CustomerInvoiceWizard(models.Model):
    _name = 'customer.wizard'

    partner_id = fields.Many2one('res.partner', 'Customer')
    date_from = fields.Date('Date From')
    date_to = fields.Date('Date To')
    type = fields.Selection([('out_invoice','Sales Invoice'),('packing_slip','Packing Slip'),('holding_invoice','Holding Invoice'),('out_refund','Credit Note'),('in_refund','Debit Note')])
    invoice_wizard_ids = fields.One2many('account.invoice.wizard','customer_id')
    invoice_id = fields.Many2one('account.invoice','invoice_id')
    cus_invoice_ids = fields.One2many('wizard.invoice', 'customer_wizard', 'Invoices')

    @api.multi
    def get_invoice_details(self):
        self.ensure_one()
        self.cus_invoice_ids = [(5, 0, 0)]  

        if self.date_from and self.date_to:
            invoice_domain = [('date_invoice', '>=', self.date_from),
                              ('date_invoice', '<=', self.date_to)]
        if self.partner_id:
            invoice_domain.append(('partner_id', '=', self.partner_id.id))
        if self.type == 'out_invoice':
            invoice_domain.append(('type', '=', 'out_invoice'))
        if self.type == 'packing_slip':
            invoice_domain.append(('packing_invoice', '=', True))
        if self.type == 'holding_invoice':
            invoice_domain.append(('holding_invoice', '=', True))
        if self.type == 'out_refund':
            invoice_domain.append(('type', '=', 'out_refund'))
        if self.type == 'in_refund':
            invoice_domain.append(('type', '=', 'in_refund'))

        invoices = self.env['account.invoice'].search(invoice_domain)
        line_values = []
        for i in invoices:
            line_values.append((0, 0, {
                'partner_id': i.partner_id.id,
                'active_invoice_id': self.invoice_id.id,
                'invoice_id': i.id,
                'date_invoice': i.date_invoice,
                'res_person': i.res_person.id,
                'cus_inv_number': i.cus_inv_number,
                'residual': i.residual,
                'amount_untaxed': i.amount_untaxed,
                'amount_total': i.amount_total,
                'type': 'invoice'
            }))
        self.cus_invoice_ids = line_values

        # return {
        #     'type': 'ir.actions.act_window',
        #     'res_model': 'customer.wizard',
        #     'view_mode': 'form',
        #     'view_type': 'form',
        #     'res_id': self.id,
        #     'target': 'new',
        # }

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
            if self.type =='out_refund':
                domain.append(('invoice_id.type','=','out_refund'))
            if self.type =='in_refund':
                domain.append(('invoice_id.type','=','in_refund'))

            invoice_lines = self.env['account.invoice.line'].search(domain)
            line_values = []
            for rec in invoice_lines:
                line_values.append((0, 0, {
                    'id_for_ref': rec.id_for_ref,
                    'stock_entry_id': rec.stock_entry_id.id,
                    'name': rec.name,
                    'product_id': rec.product_id.id,
                    'medicine_name_subcat': rec.medicine_name_subcat.id,
                    'medicine_name_packing': rec.medicine_name_packing.id,
                    'product_of': rec.product_of.id,
                    'medicine_grp': rec.medicine_grp.id,
                    'batch_2': rec.batch_2.id,
                    'batch': rec.batch,
                    'hsn_code': rec.hsn_code,
                    'price_unit': rec.price_unit,
                    'discount': rec.discount or 0,
                    'manf_date': rec.manf_date,
                    'expiry_date': rec.expiry_date,
                    'medicine_rack': rec.medicine_rack.id,
                    'invoice_line_tax_id4': rec.invoice_line_tax_id4,
                    'rack_qty': rec.rack_qty,
                    'quantity': rec.quantity,
                    'invoice_id': rec.invoice_id.id,

                }))
            self.invoice_wizard_ids = line_values
            # print(line_values, 'product')
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'customer.wizard',
                'view_mode': 'form',
                'view_type': 'form',
                'res_id': self.id,
                'target': 'new',
            }

    @api.multi
    def add_selected_lines(self):
        selected_lines = self.invoice_wizard_ids.filtered(lambda x: x.selected)
        if selected_lines:
            new_lines = []
            for rec in selected_lines:
                new_lines.append((0, 0, {
                    'id_for_ref': rec.id_for_ref,
                    'stock_entry_id': rec.stock_entry_id.id,
                    'name': rec.name,
                    'product_id': rec.product_id.id,
                    'medicine_name_subcat': rec.medicine_name_subcat.id,
                    'medicine_name_packing': rec.medicine_name_packing.id,
                    'product_of': rec.product_of.id,
                    'medicine_grp': rec.medicine_grp.id,
                    'batch_2': rec.batch_2.id,
                    'batch': rec.batch,
                    'hsn_code': rec.hsn_code,
                    'price_unit': rec.price_unit,
                    'discount': rec.discount or 0,
                    'manf_date': rec.manf_date,
                    'expiry_date': rec.expiry_date,
                    'medicine_rack': rec.medicine_rack.id,
                    'invoice_line_tax_id4': rec.invoice_line_tax_id4,
                    'rack_qty': rec.rack_qty,
                    'quantity': rec.quantity,
                    'invoice_id': rec.invoice_id.id,
                }))
            invoice_id = self.env['account.invoice'].browse([(self.invoice_id.id)])
            if invoice_id:
                invoice_id.write({'invoice_line': new_lines})

    @api.multi
    def add_all_lines(self):
        if self.invoice_wizard_ids:
            new_lines = []
            for rec in self.invoice_wizard_ids:
                new_line = {
                    'id_for_ref': rec.id_for_ref,
                    'stock_entry_id': rec.stock_entry_id.id,
                    'name': rec.name,
                    'product_id': rec.product_id.id,
                    'medicine_name_subcat': rec.medicine_name_subcat.id,
                    'medicine_name_packing': rec.medicine_name_packing.id,
                    'product_of': rec.product_of.id,
                    'medicine_grp': rec.medicine_grp.id,
                    'batch_2': rec.batch_2.id,
                    'batch': rec.batch,
                    'hsn_code': rec.hsn_code,
                    'price_unit': rec.price_unit,
                    'discount': rec.discount or 0,
                    'manf_date': rec.manf_date,
                    'expiry_date': rec.expiry_date,
                    'medicine_rack': rec.medicine_rack.id,
                    'invoice_line_tax_id4': rec.invoice_line_tax_id4,
                    'rack_qty': rec.rack_qty,
                    'quantity': rec.quantity,
                    'invoice_id': rec.invoice_id.id,
                }
                new_lines.append((0, 0, new_line))

            if self.invoice_id:
                self.invoice_id.write({'invoice_line': new_lines})


class AccountInvoiceLineWizhard(models.Model):
    _name = "account.invoice.wizard"
    _rec_name = 'id'

    customer_id = fields.Many2one('customer.wizard')
    wizard_id = fields.Many2one('wizard.invoice')
    invoice_id = fields.Many2one('account.invoice.line')
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
    quantity = fields.Integer('Qty')
    price_unit = fields.Float(string='Mrp')
    unit_price_c = fields.Float(string='Unit TP', default=False)
    unit_price = fields.Float(string='Unit P')
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
    selected = fields.Boolean('selected')
    batch_2 = fields.Many2one('med.batch', "Batch")
    expiry_date = fields.Date(string='Exp')
    manf_date = fields.Date(string='Mfd')
    medicine_rack = fields.Many2one('product.medicine.types', 'Rack')
    rack_qty = fields.Float(string="stock",)


class AccountWizhardInvoice(models.Model):
    _name = "wizard.invoice"
    _rec_name = 'id'

    customer_wizard = fields.Many2one('customer.wizard')
    partner_id = fields.Many2one('res.partner', create=True)
    date_invoice = fields.Date(string="Invoice Date")
    res_person = fields.Many2one('res.partner', string="Responsible Person")
    cus_inv_number = fields.Char()
    residual = fields.Float()
    amount_untaxed = fields.Float()
    amount_total = fields.Float()
    active_invoice_id = fields.Many2one('account.invoice')
    invoice_id = fields.Many2one('account.invoice')
    invoice_wizard_ids = fields.One2many('account.invoice.wizard','wizard_id')


    @api.multi
    def get_details(self):
        self.ensure_one()
        invoice = self.env['account.invoice'].browse([(self.invoice_id.id)])
        line_values = []
        for rec in invoice.invoice_line:
            line_values.append((0, 0, {
                'id_for_ref': rec.id_for_ref,
                'stock_entry_id': rec.stock_entry_id.id,
                'name': rec.name,
                'product_id': rec.product_id.id,
                'medicine_name_subcat': rec.medicine_name_subcat.id,
                'medicine_name_packing': rec.medicine_name_packing.id,
                'product_of': rec.product_of.id,
                'medicine_grp': rec.medicine_grp.id,
                'batch_2': rec.batch_2.id,
                'batch': rec.batch,
                'hsn_code': rec.hsn_code,
                'price_unit': rec.price_unit,
                'discount': rec.discount or 0,
                'manf_date': rec.manf_date,
                'expiry_date': rec.expiry_date,
                'medicine_rack': rec.medicine_rack.id,
                'invoice_line_tax_id4': rec.invoice_line_tax_id4,
                'rack_qty': rec.rack_qty,
                'quantity': rec.quantity,
                'invoice_id': rec.invoice_id.id,

            }))
        if self.active_invoice_id:
            self.active_invoice_id.write({'invoice_line': line_values})
            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            redirect_url = "%s/web#id=%d&view_type=form&model=account.invoice&menu_id=331&action=400" % (
                base_url, self.active_invoice_id.id)
            return {
                'type': 'ir.actions.act_url',
                'url': redirect_url,
                'target': 'self',
            }

    @api.multi
    def open_invoice(self):
        return {
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.invoice_id.id,
            'res_model': 'account.invoice',
            'view_id': self.env.ref('account.invoice_form').id,
            'type': 'ir.actions.act_window',
            'flags': {'action_buttons': True},
            'target': 'new',
        }






