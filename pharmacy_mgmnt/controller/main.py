from openerp import http
from openerp.http import request
import json


class SupplierProductInvoiceline(http.Controller):

    @http.route('/pharmacy_mgmnt/reset_quantity', auth='user')
    def reset_quantity_selected(self):

        records = request.env['entry.stock'].search([])
        # Call the method on each record
        for record in records:
            record.reset_quantity_selected()

        return json.dumps({'success': True})

