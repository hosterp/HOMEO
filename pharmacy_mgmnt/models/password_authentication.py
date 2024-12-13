from openerp import models, fields, api, exceptions, _

class InvoicePasswordWizard(models.TransientModel):
    _name = 'invoice.password.wizard'
    _description = 'Password Authentication Wizard'

    password = fields.Char(string="Password", required=True, help="Enter your password", password="True")
    invoice_id = fields.Many2one('account.invoice', string="Invoice")

    @api.multi
    def confirm_password(self):
        """Logic for password confirmation."""
        self.ensure_one()
        current_user = self.env.user  # Get the current logged-in user
        try:
            self.env['res.users'].check_credentials(self.password)
        except Exception:
            raise Warning("Incorrect Password!")

        # If the password is correct, add your custom logic here
        self.invoice_id.write({'state': 'confirmed'})
