from openerp import models, fields, api


class SupplierInvoiceWizard(models.Model):
    _name = 'supplier.wizard'

    partner_id = fields.Many2one('res.partner', string='Supplier', domain="[('supplier', '=', True)]")
    date_from = fields.Date('Date From', required=True)
    date_to = fields.Date('Date To', required=True)
    type = fields.Selection([('in_invoice', 'Supplier Invoice'), ('in_refund', 'Debit Note')])
    invoice_id = fields.Many2one('account.invoice', 'invoice_id')
    invoice_wizard_ids = fields.One2many('account.invoice.wizard.supplier', 'supplier_id', string='Invoice Wizard Lines')
    cus_invoice_ids = fields.One2many('wizard.invoice.supplier', 'supplier_wizard', string='Supplier Invoices')

    @api.multi
    def get_invoice_details(self):
        self.ensure_one()
        self.cus_invoice_ids = [(5, 0, 0)]

        invoice_domain = [('date_invoice', '>=', self.date_from),('date_invoice', '<=', self.date_to)]

        if self.partner_id:
            invoice_domain.append(('partner_id', '=', self.partner_id.id))
        if self.type == 'in_refund':
            invoice_domain.append(('type', '=', 'in_refund'))
        if self.type == 'in_invoice':
            invoice_domain.append(('type', '=', 'in_invoice'))

        invoices = self.env['account.invoice'].search(invoice_domain)
        # print(invoices,'invoices.........................')
        line_values = []
        for inv in invoices:
            line_values.append((0, 0, {
                'partner_id': inv.partner_id.id,
                'active_invoice_id': self.invoice_id.id,
                'invoice_id': inv.id,
                'date_invoice': inv.date_invoice,
                # 'res_person': inv.res_person.id,
                'cus_inv_number': inv.cus_inv_number,
                'residual': inv.residual,
                'amount_untaxed': inv.amount_untaxed,
                'amount_total': inv.amount_total,
                'type': 'invoice'
            }))
        self.cus_invoice_ids = line_values
        # print(line_values,'line valuessssss..............')

    @api.multi
    def get_details(self):
        self.ensure_one()
        self.invoice_wizard_ids = [(5, 0, 0)]

        domain = [('create_date', '>=', self.date_from), ('create_date', '<=', self.date_to)]
        if self.partner_id:
            domain.append(('partner_id', '=', self.partner_id.id))
        if self.type == 'in_refund':
            domain.append(('type', '=', 'in_refund'))
        if self.type == 'in_invoice':
            domain.append(('type', '=', 'in_invoice'))
        invoice_lines = self.env['account.invoice.line'].search(domain)
        line_values = []
        for inv in invoice_lines:
            line_values.append((0, 0, {
                'id_for_ref': inv.id_for_ref,
                'stock_entry_id': inv.stock_entry_id.id,
                'name': inv.name,
                'product_id': inv.product_id.id,
                'medicine_name_subcat': inv.medicine_name_subcat.id,
                'medicine_name_packing': inv.medicine_name_packing.id,
                'product_of': inv.product_of.id,
                'medicine_grp': inv.medicine_grp.id,
                'batch_2': inv.batch_2.id,
                'batch': inv.batch,
                'hsn_code': inv.hsn_code,
                'price_unit': inv.price_unit,
                'discount': inv.discount or 0,
                'discount3': inv.discount3 or 0,
                'manf_date': inv.manf_date,
                'expiry_date': inv.expiry_date,
                'medicine_rack': inv.medicine_rack.id,
                'invoice_line_tax_id4': inv.invoice_line_tax_id4,
                'rack_qty': inv.rack_qty,
                'quantity': inv.quantity,
                'invoice_id': inv.invoice_id.id,
            }))
        self.invoice_wizard_ids = line_values
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'supplier.wizard',
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
            for line in selected_lines:
                new_lines.append((0, 0, {
                    'stock_entry_id': line.stock_entry_id.id,
                    'name': line.name,
                    'product_id': line.product_id.id,
                    'medicine_name_subcat': line.medicine_name_subcat.id,
                    'medicine_name_packing': line.medicine_name_packing.id,
                    'product_of': line.product_of.id,
                    'medicine_grp': line.medicine_grp.id,
                    'batch_2': line.batch_2.id,
                    'batch': line.batch,
                    'hsn_code': line.hsn_code,
                    'price_unit': line.price_unit,
                    'discount': line.discount or 0,
                    'manf_date': line.manf_date,
                    'expiry_date': line.expiry_date,
                    'medicine_rack': line.medicine_rack.id,
                    'invoice_line_tax_id4': line.invoice_line_tax_id4,
                    'rack_qty': line.rack_qty,
                    'quantity': line.quantity,
                    'invoice_id': line.invoice_id.id,
                }))
            if self.invoice_id:
                self.invoice_id.write({'invoice_line': new_lines})

    @api.multi
    def add_all_lines(self):
        print("Called add_all_lines in SupplierInvoiceWizard")
        active_invoice = self.env['account.invoice'].browse(self.invoice_id.id)
        print(active_invoice, self.invoice_id.id, 'print active...................')

        if self.invoice_wizard_ids:
            print('hai')
            new_lines = []
            for line in self.invoice_wizard_ids:
                new_line = {
                    'stock_entry_id': line.stock_entry_id.id,
                    # 'name': line.name,
                    'product_id': line.product_id.id,
                    'medicine_name_subcat': line.medicine_name_subcat.id,
                    'medicine_name_packing': line.medicine_name_packing.id,
                    'product_of': line.product_of.id,
                    'medicine_grp': line.medicine_grp.id,
                    'batch': line.batch,
                    'hsn_code': line.hsn_code,
                    'price_unit': line.price_unit,
                    'unit_price_s': line.unit_price_s,
                    'discount3': line.discount3 or 0,
                    'manf_date': line.manf_date,
                    'expiry_date': line.expiry_date,
                    'medicine_rack': line.medicine_rack.id,
                    'invoice_line_tax_id4': line.invoice_line_tax_id4,
                    'amount_w_tax': line.amount_w_tax,
                    'quantity': line.quantity,
                    'invoice_id': line.invoice_id.id,
                }
                new_lines.append((0, 0, new_line))

            if self.invoice_id:
                # Ensure the correct field name is used (invoice_line_ids might be the correct one)
                self.invoice_id.write({'invoice_line': new_lines})  # or 'invoice_line': new_lines
                print("New lines written to invoice:", new_lines)


class AccountInvoiceLineWizard(models.TransientModel):
    _name = "account.invoice.wizard.supplier"
    _rec_name = 'id'

    supplier_id = fields.Many2one('supplier.wizard')
    wizard_id = fields.Many2one('wizard.invoice.supplier', string='Invoice Line')
    name = fields.Text(string="Description", required=False)
    stock_entry_id = fields.Many2one('entry.stock', string='Stock Entry')
    stock_entry_qty = fields.Float(string='Stock Entry Quantity')
    product_id = fields.Many2one('product.product', string='Medicine')
    medicine_name_subcat = fields.Many2one('product.medicine.subcat', string='Potency')
    batch = fields.Char(string="Batch")
    medicine_name_packing = fields.Many2one('product.medicine.packing', string='Pack')
    product_of = fields.Many2one('product.medicine.responsible', string='Company')
    medicine_grp = fields.Many2one('product.medicine.group', string='Group')
    stock_transfer_id = fields.Many2one('stock.transfer', string='Stock Transfer')
    quantity = fields.Integer(string='Quantity')
    price_unit = fields.Float(string='Unit Price')
    invoice_line_tax_id4 = fields.Float(string='Tax')
    amount_amount = fields.Float(string='Tax Amount')
    amount_w_tax = fields.Float(string='Total Amount')
    discount = fields.Float(default=0.0)
    discount2 = fields.Float(string="Discount 2")
    discount3 = fields.Float(string="Discount 3")
    discount4 = fields.Float(string="Discount 4")
    # amount_w_tax = fields.Float()
    unit_price_s = fields.Float()
    id_for_ref = fields.Integer()
    product_tax = fields.Float(string='Tax Amount')
    price_subtotal = fields.Float(string='Subtotal')
    hsn_code = fields.Char(string='HSN Code')
    selected = fields.Boolean(string='Selected')
    batch_2 = fields.Many2one('med.batch', string="Batch 2")
    expiry_date = fields.Date(string='Expiry Date')
    manf_date = fields.Date(string='Manufacture Date')
    medicine_rack = fields.Many2one('product.medicine.types', string='Rack')
    rack_qty = fields.Float(string="Rack Quantity")


class AccountWizardInvoiceSupplier(models.TransientModel):
    _name = "wizard.invoice.supplier"
    _rec_name = 'id'

    supplier_wizard = fields.Many2one('supplier.wizard', string='Supplier Wizard')
    partner_id = fields.Many2one('res.partner', string='Partner', create=True)
    date_invoice = fields.Date(string="Invoice Date")
    cus_inv_number = fields.Char(string="Customer Invoice Number")
    residual = fields.Float(string="Residual")
    amount_untaxed = fields.Float(string="Untaxed Amount")
    amount_total = fields.Float(string="Total Amount")
    active_invoice_id = fields.Many2one('account.invoice', string='Active Invoice')
    invoice_id = fields.Many2one('account.invoice', string='Invoice')
    supplier_invoice_wizard_ids = fields.One2many('account.invoice.wizard.supplier', 'wizard_id')

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
                'unit_price_s': rec.unit_price_s,
                'batch_2': rec.batch_2.id,
                'batch': rec.batch,
                'hsn_code': rec.hsn_code,
                'price_unit': rec.price_unit,
                'discount': rec.discount or 0,
                'discount3': rec.discount3 or 0,
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
            self.active_invoice_id.write({'partner_id': self.invoice_id.partner_id.id})
            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            redirect_url = "%s/web#id=%d&view_type=form&model=account.invoice&menu_id=328&action=399" % (
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
            'view_id': self.env.ref('account.invoice_supplier_form').id,
            'type': 'ir.actions.act_window',
            'flags': {'action_buttons': True},
            'target': 'new',
        }

    @api.multi
    def add_all_lines(self):
        self.ensure_one()
        active_invoice = self.env['account.invoice'].browse(self.invoice_id.id)
        print("Active invoice:", active_invoice)

        new_lines = []
        for line in active_invoice.invoice_line:
            print("Processing line:", line)
            new_line = {
                'stock_entry_id': line.stock_entry_id.id,
                # Uncomment if 'name' is a valid field in account.invoice.line
                'name': line.name,
                'product_id': line.product_id.id,
                'medicine_name_subcat': line.medicine_name_subcat.id,
                'medicine_name_packing': line.medicine_name_packing.id,
                'product_of': line.product_of.id,
                'medicine_grp': line.medicine_grp.id,
                'batch': line.batch,
                'hsn_code': line.hsn_code,
                'price_unit': line.price_unit,
                'unit_price_s': line.unit_price_s,
                'discount3': line.discount3 or 0,
                'manf_date': line.manf_date,
                'expiry_date': line.expiry_date,
                'medicine_rack': line.medicine_rack.id,
                'invoice_line_tax_id4': line.invoice_line_tax_id4,
                'amount_w_tax': line.amount_w_tax,
                'quantity': line.quantity,
                'invoice_id': line.invoice_id.id,
            }
            new_lines.append((0, 0, new_line))
        self.active_invoice_id.write({'invoice_line': new_lines})
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.invoice',
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': self.active_invoice_id.id,
            'target': 'current',
        }

    # @api.multi
    # def add_all_lines(self):
    #     print("Called add_all_lines in SupplierInvoiceWizard")
    #     active_invoice = self.env['account.invoice'].browse(self.invoice_id.id)
    #     print(active_invoice, self.invoice_id.id, 'print active...................')
    #
    #     if self.supplier_invoice_wizard_ids:
    #         print('hai')
    #         new_lines = []
    #         for line in self.supplier_invoice_wizard_ids:
    #             new_line = {
    #                 'stock_entry_id': line.stock_entry_id.id,
    #                 # 'name': line.name,
    #                 'product_id': line.product_id.id,
    #                 'medicine_name_subcat': line.medicine_name_subcat.id,
    #                 'medicine_name_packing': line.medicine_name_packing.id,
    #                 'product_of': line.product_of.id,
    #                 'medicine_grp': line.medicine_grp.id,
    #                 'batch': line.batch,
    #                 'hsn_code': line.hsn_code,
    #                 'price_unit': line.price_unit,
    #                 'unit_price_s': line.unit_price_s,
    #                 'discount3': line.discount3 or 0,
    #                 'manf_date': line.manf_date,
    #                 'expiry_date': line.expiry_date,
    #                 'medicine_rack': line.medicine_rack.id,
    #                 'invoice_line_tax_id4': line.invoice_line_tax_id4,
    #                 'amount_w_tax': line.amount_w_tax,
    #                 'quantity': line.quantity,
    #                 'invoice_id': line.invoice_id.id,
    #             }
    #             new_lines.append((0, 0, new_line))
    #
    #         if self.invoice_id:
    #             # Ensure the correct field name is used (invoice_line_ids might be the correct one)
    #             self.invoice_id.write({'invoice_line': new_lines})  # or 'invoice_line': new_lines
    #             print("New lines written to invoice:", new_lines)
