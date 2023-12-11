try:
    from openerp.addons.report_xlsx.report.report_xlsx import ReportXlsx
except ImportError:
    class ReportXlsx(object):
        def __init__(self, *args, **kwargs):
            pass
from datetime import datetime
class BtobHsnXlsx(ReportXlsx):
    def generate_xlsx_report(self, workbook, data, lines):
        if lines.type == 'interstate':
            partner_ids = lines.env['res.partner'].search([
                ('b2b', '=', True), ('interstate_customer', '=', True)])
        elif lines.type == 'local':
            partner_ids = lines.env['res.partner'].search([
                ('b2b', '=', True), ('interstate_customer', '=', False)])
        else:
            partner_ids = lines.env['res.partner'].search([
                ('b2b', '=', True)])

        invoice_ids = lines.env['account.invoice'].search([
            ('date_invoice', '>=', lines.from_date),
            ('date_invoice', '<=', lines.to_date),
            ('partner_id', 'in', partner_ids.ids),
            ('packing_slip', '=', False),
            ('holding_invoice', '=', False),
            ('type', '=', 'out_invoice'),
            ('state', '=', 'paid')
        ])


        format = workbook.add_format({'font_size':13,'align':'vcentre','bold':True})
        format1 = workbook.add_format({'font_size':11,'align':'vcentre','bold':True})
        format2 = workbook.add_format({'font_size':9,'align':'vcentre','bold':True})
        sl_no_format = workbook.add_format({'font_size': 9, 'align': 'left', 'bold': True})
        format3 = workbook.add_format({'font_size':9,'align':'vcentre','bold':False})
        format4 = workbook.add_format({'font_size':9,'align':'vcentre','bold':False})
        format5 = workbook.add_format({'font_size':9,'align':'vcentre','bold':True})
        sheet = workbook.add_worksheet('BTOB BILL BY DATE WISE')
        sheet.write(2, 3, "TRAVANCORE HOMEO-GST TAX REPORT", format)
        from_date_str = lines.from_date
        to_date_str = lines.to_date
        from_date = datetime.strptime(from_date_str, '%Y-%m-%d')
        to_date = datetime.strptime(to_date_str, '%Y-%m-%d')
        formatted_from_date = from_date.strftime('%d-%m-%Y')
        formatted_to_date = to_date.strftime('%d-%m-%Y')
        sheet.write(3, 2, "BTOB TAX REPORT BY HSN WISE {} - {}".format(formatted_from_date, formatted_to_date), format)
        # sheet.write(3, 3, "BTOB TAX REPORT BY HSN WISE", str(lines.from_date), '-', str(lines.to_date), format)
        # sheet.write(3, 2, "BTOB TAX REPORT BY HSN WISE {} - {}".format(lines.from_date, lines.to_date), format)

        sheet.write(5, 2, "No", format1)
        sheet.write(5, 3, "Customer", format1)
        sheet.write(5, 5, "GSTIN", format1)
        sheet.write(5, 7, "BillDate", format1)
        sheet.write(5, 8, "BillNo", format1)

        sub_head_row = 6
        bill_tax_total = 0
        bill_amount_total = 0
        tax_total = 0
        amt_total = 0
        sl_no = 1
        for rec in invoice_ids:
            sheet.write(sub_head_row, 2, sl_no ,  sl_no_format)
            sheet.write(sub_head_row, 3, rec.partner_id.name or '',  format2)
            sheet.write(sub_head_row, 5, rec.partner_id.gst_no, format2)

            date_str = rec.date_invoice
            from_date = datetime.strptime(date_str, '%Y-%m-%d')
            formatted_from_date = from_date.strftime('%d-%m-%Y')

            sheet.write(sub_head_row, 7, formatted_from_date, format2)
            sheet.write(sub_head_row, 8, rec.number2, format2)
            sub_head_row += 1
            sl_no += 1
            sheet.write(sub_head_row, 3, "HSN", format3)
            sheet.write(sub_head_row, 4, "QTY", format3)
            sheet.write(sub_head_row, 5, "TAX", format3)
            sheet.write(sub_head_row, 6, "TAX AMT", format3)
            sheet.write(sub_head_row, 7, "TOTAL", format3)
            sub_head_row += 1
            for line in rec.invoice_line:
                sheet.write(sub_head_row, 3, line.hsn_code, format4)
                sheet.write(sub_head_row, 4, line.quantity, format4)
                sheet.write(sub_head_row, 5, line.invoice_line_tax_id4, format4)
                sheet.write(sub_head_row, 6, line.product_tax, format4)
                bill_tax_total += line.product_tax
                sheet.write(sub_head_row, 7, line.amt_w_tax, format4)
                bill_amount_total += line.amt_w_tax
                sub_head_row += 1

            sheet.write(sub_head_row, 3, "Total", format5)
            sheet.write(sub_head_row, 6, bill_tax_total, format5)
            sheet.write(sub_head_row, 7, bill_amount_total, format5)
            tax_total += bill_tax_total
            amt_total += bill_amount_total
            bill_tax_total = 0
            bill_amount_total = 0
            sub_head_row += 1
        sheet.write(sub_head_row, 2, "Grand Total", format1)
        sheet.write(sub_head_row, 6, tax_total, format1)
        sheet.write(sub_head_row, 7, amt_total, format1)

BtobHsnXlsx('report.pharmacy_mgmnt.b2b_date_tax_report_template_xlsx.xlsx', 'tax.report.wizard')