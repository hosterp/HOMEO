from openerp import models, fields, api, exceptions, _
from openerp.exceptions import ValidationError


class InvoicePasswordWizard(models.Model):
    _name = 'invoice.password.wizard'
    _description = 'Password Authentication Wizard'

    password = fields.Char(string="Password", required=True, help="Enter your password", password="True")
    invoice_id = fields.Many2one('account.invoice', string="Invoice")
    user=fields.Char(string='user')

    @api.multi
    def confirm_password(self):
        print('successfully..................................')
        """Logic for password confirmation."""
        self.ensure_one()
        users = self.env['res.users'].search([])
        is_password_valid = False
        for i in users:
            print(i.rec_password, 'password.......................................................')
            if i.rec_password == self.password:
                self.user=i.name
                print(i.name,'user name............................................................')
                is_password_valid = True
                break
        if is_password_valid:
            print('Password match successful.')
            if self.invoice_id:
                self.invoice_id.write({'validated_by_user': self.user})
            return is_password_valid

        else:
            raise ValidationError("Incorrect Password!")

