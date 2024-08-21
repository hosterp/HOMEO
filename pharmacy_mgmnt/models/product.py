from openerp import models, fields, api
from openerp.exceptions import ValidationError


class ProductVariantInherit(models.Model):
    _inherit = "product.product"

    # Tax_of_pdt = fields.Char('Medicine Tax')
    Tax_of_pdt = fields.Many2many('account.tax',
                                  'account_invoice_line_tax', 'invoice_line_id', 'tax_id',
                                  string='Taxes',
                                  domain=[('parent_id', '=', False), '|', ('active', '=', False),
                                          ('active', '=', True)])

class Medicines(models.Model):
    _inherit = 'product.template'

    medicine_rack = fields.Many2one('product.medicine.types', 'Medicine Category/Rack')
    product_of = fields.Many2one('product.medicine.responsible', 'Company')
    medicine_name_subcat = fields.Many2one('product.medicine.subcat', 'Potency')
    # medicine_name_subcat = fields.Char('Potency')
    medicine_name_packing = fields.Many2one('product.medicine.packing', 'Packing')
    medicine_grp = fields.Many2one('product.medicine.group', 'Grp')
    # medicine_group = fields.Char('Group')
    batch = fields.Char("Batch")
    tax_ids = fields.Many2many('account.tax', 'name', 'Tax')
    hsn_code = fields.Char('HSN', )
    made_in = fields.Selection([('indian', 'Indian'), ('german', 'German')], default='indian', string="Made In")
    visible_in = fields.Selection([('true', 'True'), ('false', 'False')], default='false', string="Visible")
    # tax_combo = fields.Many2one('tax.combo', 'Tax')

    @api.onchange('name')
    def onchange_name_product(self):
        if self.name:
            self.visible_in == 'true'
        else:
            self.visible_in == 'false'

    @api.model
    def create(self, vals):
        # Search for existing product with the same name
        existing_product = self.search([('name', '=', vals.get('name'))], limit=1)

        if existing_product:
            # Update existing product if found
            existing_product.write(vals)
            return existing_product
        else:
            # Create new product if no existing product found
            return super(Medicines, self).create(vals)

    @api.constrains('name')
    def _check_name_product(self):
        for record in self:
            # Search for records with the same name excluding the current record
            existing_records = self.search([('name', '=', record.name), ('id', '!=', record.id)])
            if existing_records:
                raise ValidationError('Product with this name already exists.')



    @api.onchange('medicine_name_subcat')
    def onchange_ref_id(self):
        for rec in self:
            pass

    # Tax_of_pdt = fields.Char('Medicine Tax')
    Tax_of_pdt = fields.Many2many('account.tax',
                                  'account_invoice_line_tax', 'invoice_line_id', 'tax_id',
                                  string='Taxes',
                                  domain=[('parent_id', '=', False), '|', ('active', '=', False),
                                          ('active', '=', True)])

