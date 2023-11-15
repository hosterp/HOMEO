from openerp import api, models, fields
from openerp.osv import osv

class MedicineEnquiry(models.Model):
    _name = "medicine.enquiry"
    _description = 'Medicine Enquiry'


    name = fields.Many2one("res.partner", string="Customer", domain="[('customer', '=', True)]")
    phone_no = fields.Char(string="Phone Number")
    address = fields.Char(string="Address")
    medicine_ids = fields.One2many("medicine.enquiry.line", "medicine_line_id")

    @api.onchange("name")
    def onchange_name(self):
        if self.name:
            self.address = self.name.address_new
            self.phone_no = self.name.mobile


class MedicineEnquiryLine(models.Model):
    _name = "medicine.enquiry.line"
    _description = 'Medicine Enquiry Line'

    medicine_line_id = fields.Many2one("medicine.enquiry", string="Medicine Entry")
    medicine_id = fields.Many2one("product.product", string="Medicine")
    group_id = fields.Many2one("product.medicine.group", string="Group")
    potency_id = fields.Many2one("product.medicine.subcat", string="Potency")
    packing_id = fields.Many2one("product.medicine.packing", string="Packing")

