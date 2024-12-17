from openerp import http,_
from openerp.exceptions import ValidationError
from openerp.http import request
from werkzeug.wrappers import Response
import json


class SupplierProductInvoiceline(http.Controller):

    @http.route('/pharmacy_mgmnt/reset_quantity', auth='user')
    def reset_quantity_selected(self):

        records = request.env['entry.stock'].search([])

        for record in records:
            record.reset_quantity_selected()

        return json.dumps({'success': True})

class PaymentHistory(http.Controller):
    @http.route('/pharmacy_mgmnt/payment_history', auth='user', type='json', website=True)
    def payment_history_invoiceline(self):
        env = request.env  # Access the Odoo environment

        # Search for all partner payment records
        partner_payments = env['invoice.details'].search([])

        # Initialize a list to store payment history data
        payment_history_data = []

        # Loop through each partner payment record
        for partner_payment in partner_payments:
            # Fetch associated invoice lines for this partner payment
            invoice_lines = partner_payment.invoice_id

            # Prepare data for this partner payment
            data = {
                'id': partner_payment.id,
                'name': partner_payment.name,
                'invoice_id': [(6, 0, invoice_lines.ids)]
            }

            # Append this data to the list
            payment_history_data.append(data)
            print(payment_history_data,'payment')

        # Define the JSON response including the tree view data
        json_response = {
            'payment_history_data': payment_history_data,
            'success': True,
            'view_id': env.ref('pharmacy_mgmnt.view_invoice_details_tree').id,
            'type': 'ir.actions.act_window',
            'target': 'current',
            'res_model': 'invoice.details',
            'view_mode': 'tree',
        }

        return json_response
class CustomPasswordValidationController(http.Controller):

    @http.route('/password/validate', type='json', auth='public', methods=['POST'])
    def validate_password(self,**kw):
        try:
            password = request.jsonrequest.get('password')
            if not password:
                raise ValidationError("Password is missing!")

            print("Password received in controller:", password)


            users = request.env['res.users'].sudo().search([])
            is_password_valid = any(user.rec_password == password for user in users)

            if is_password_valid:
                return {'password_valid': True}
            else:
                return {'password_valid': False, 'error_message': 'Incorrect Password!'}

        except Exception as e:
            return {'password_valid': False, 'error_message': str(e)}