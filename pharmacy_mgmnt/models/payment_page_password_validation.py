from openerp import models, fields, api, exceptions, _
from openerp.exceptions import ValidationError


class InvoicePasswordWizard(models.Model):
    _name = 'payment.password.wizard'
    _description = 'Password Authentication Wizard'

    password = fields.Char(string="Password", required=True, help="Enter your password", password="True")
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
            return is_password_valid

        else:
            raise ValidationError("Incorrect Password!")

