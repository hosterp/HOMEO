try:
    from openerp.addons.report_xlsx.report.report_xlsx import ReportXlsx
except ImportError:
    class ReportXlsx(object):
        def __init__(self, *args, **kwargs):
            pass

class BtocHsnXlsx(ReportXlsx):
    def generate_xlsx_report(self, workbook, data, lines):
        if lines.type == 'interstate':
            partner_ids = lines.env['res.partner'].search([
                ('b2c', '=', True), ('interstate_customer', '=', True)])
        elif lines.type == 'local':
            partner_ids = lines.env['res.partner'].search([
                ('b2c', '=', True), ('interstate_customer', '=', False)])
        else:
            partner_ids = lines.env['res.partner'].search([
                ('b2c', '=', True)])

        invoice_ids = lines.env['account.invoice'].search([
            ('date_invoice', '>=', lines.from_date),
            ('partner_id', 'in', partner_ids.ids),
            ('date_invoice', '<=', lines.to_date),
            ('packing_slip', '=', False),
            ('holding_invoice', '=', False),
            ('type', '=', 'out_invoice'),
            ('state', '=', 'paid')
        ])
        data_dict = {}
        for invoice in invoice_ids:
            for rec in invoice.invoice_line:
                hsn_code = rec.hsn_code
                invoice_line_tax_id4 = rec.invoice_line_tax_id4
                key = (hsn_code, invoice_line_tax_id4)
                if key in data_dict:
                    data_dict[key]['quantity'] += rec.quantity
                    data_dict[key]['product_tax'] += rec.product_tax
                    data_dict[key]['amt_w_tax'] += rec.amt_w_tax
                else:
                    data_dict[key] = {
                        'hsn_code': hsn_code,
                        'invoice_line_tax_id4': invoice_line_tax_id4,
                        'quantity': rec.quantity,
                        'product_tax': rec.product_tax,
                        'amt_w_tax': rec.amt_w_tax,
                    }
        data_list = [{'invoice_data': [vals]} for vals in data_dict.values()]



        format = workbook.add_format({'font_size':13,'align':'vcentre','bold':True})
        format1 = workbook.add_format({'font_size':11,'align':'vcentre','bold':True})
        format2 = workbook.add_format({'font_size':9,'align':'vcentre','bold':True})
        format3 = workbook.add_format({'font_size':9,'align':'vcentre','bold':False})
        sheet = workbook.add_worksheet('BTOB BILL BY DATE WISE')
        sheet.write(2, 3, "TRAVANCORE HOMEO-GST TAX REPORT", format)
        sheet.write(3, 2, "BTOC TAX REPORT BY HSN WISE {} - {}".format(lines.from_date, lines.to_date), format)
        sheet.write(5, 2, "ItemDescri", format1)
        sheet.write(5, 4, "CountOfQT", format1)
        sheet.write(5, 6, "TaxPer", format1)
        sheet.write(5, 7, "TotalTAX", format1)
        sheet.write(5, 9, "TotalAMT", format1)
        row = 6
        total_tax = 0
        total_amt = 0
        for rec in data_list:
            for data in rec['invoice_data']:
                sheet.write(row, 2, data['hsn_code'], format3)
                sheet.write(row, 4, data['quantity'], format3)
                sheet.write(row, 6, data['invoice_line_tax_id4'], format3)
                sheet.write(row, 7, data['product_tax'], format3)
                total_tax += data['product_tax']
                sheet.write(row, 9, data['amt_w_tax'], format3)
                total_amt += data['product_tax']
                row += 1
        sheet.write(row, 2, 'Total', format2)
        sheet.write(row, 7, total_tax, format2)
        sheet.write(row, 9, total_amt, format2)

BtocHsnXlsx('report.pharmacy_mgmnt.b2c_hsn_tax_report_template_xlsx.xlsx', 'tax.report.wizard')