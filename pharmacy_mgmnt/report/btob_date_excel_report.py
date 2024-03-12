try:
    from openerp.addons.report_xlsx.report.report_xlsx import ReportXlsx
except ImportError:
    class ReportXlsx(object):
        def __init__(self, *args, **kwargs):
            pass
from datetime import datetime
class BtobDateXlsx(ReportXlsx):
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
        invoices = lines.env['account.invoice'].search(
            [("date_invoice", ">=", lines.from_date), ("date_invoice", "<=", lines.to_date),
             ('partner_id.customer', '=', True), ('partner_id', 'in', partner_ids.ids),
             ('packing_slip', '=', False), ('holding_invoice', '=', False),
             ('type', '=', 'out_invoice'),
             ('state', '=', 'paid')])
        data_list = []
        for invoice in invoices:
            tax_5 = invoice.invoice_line.filtered(lambda l: l.invoice_line_tax_id4 == 5)
            tax_12 = invoice.invoice_line.filtered(lambda l: l.invoice_line_tax_id4 == 12)
            tax_18 = invoice.invoice_line.filtered(lambda l: l.invoice_line_tax_id4 == 18)

            tax_5_sum = sum(tax_5.mapped('amt_w_tax'))
            tax_12_sum = sum(tax_12.mapped('amt_w_tax'))
            tax_18_sum = sum(tax_18.mapped('amt_w_tax'))

            total_amount_sgst_5 = (tax_5_sum * 0.05) / 2
            total_amount_sgst_12 = (tax_12_sum * 0.12) / 2
            total_amount_sgst_18 = (tax_18_sum * 0.18) / 2

            total_amount_cgst_5 = (tax_5_sum * 0.05) / 2
            total_amount_cgst_12 = (tax_12_sum * 0.12) / 2
            total_amount_cgst_18 = (tax_18_sum * 0.18) / 2

            vals = {'invoice': invoice,

                    'tax_5_sum': tax_5_sum,
                    'tax_12_sum': tax_12_sum,
                    'tax_18_sum': tax_18_sum,

                    'total_amount_sgst_5': total_amount_sgst_5,
                    'total_amount_sgst_12': total_amount_sgst_12,
                    'total_amount_sgst_18': total_amount_sgst_18,

                    'total_amount_cgst_5': total_amount_cgst_5,
                    'total_amount_cgst_12': total_amount_cgst_12,
                    'total_amount_cgst_18': total_amount_cgst_18}
            data_list.append(vals)
        format = workbook.add_format({'font_size':14,'align':'vcentre','bold':True})
        format1 = workbook.add_format({'font_size':10,'align':'vcentre','bold':True})
        format2 = workbook.add_format({'font_size':8,'align':'vcentre','bold':False})
        format3 = workbook.add_format({'font_size':9,'align':'vcentre','bold':True})
        sheet = workbook.add_worksheet('BTOB BILL BY DATE WISE')
        sheet.write(2, 4, "TRAVANCORE HOMEO-GST TAX REPORT", format)
        from_date_str = lines.from_date
        to_date_str = lines.to_date
        from_date = datetime.strptime(from_date_str, '%Y-%m-%d')
        to_date = datetime.strptime(to_date_str, '%Y-%m-%d')
        formatted_from_date = from_date.strftime('%d-%m-%Y')
        formatted_to_date = to_date.strftime('%d-%m-%Y')
        sheet.write(3, 2, "BTOB TAX REPORT BY BILL WISE {} - {}".format(formatted_from_date, formatted_to_date),
                    format)
        # sheet.write(3, 2, "BTOB TAX REPORT BY BILL WISE", format)

        sheet.write(5, 0,"DATE",format1)
        sheet.write(5, 1,"Bill No",format1)
        sheet.write(5, 2,"Customer",format1)
        sheet.write(5, 3,"GST",format1)
        sheet.write(5, 4,"Sales5%",format1)
        sheet.write(5, 5,"CGST",format1)
        sheet.write(5, 6,"IGST",format1)
        sheet.write(5, 7,"Sales12%",format1)
        sheet.write(5, 8,"CGST",format1)
        sheet.write(5, 9,"IGST",format1)
        sheet.write(5, 10,"Sales18%",format1)
        sheet.write(5, 11,"CGST",format1)
        sheet.write(5, 12,"IGST",format1)
        sheet.write(5, 13,"Bill AMOUNT",format1)
        row = 6
        bill_total = 0
        all_bill_total = 0
        tax_5_total = 0
        tax_12_total = 0
        tax_18_total = 0
        cgst_5 = 0
        igst_5 = 0
        cgst_12 = 0
        igst_12 = 0
        cgst_18 = 0
        igst_18 = 0
        for rec in data_list:
            date_str = rec['invoice'].date_invoice
            from_date = datetime.strptime(date_str, '%Y-%m-%d')
            formatted_from_date = from_date.strftime('%d-%m-%Y')

            sheet.write(row, 0, formatted_from_date, format2)
            sheet.write(row, 1, rec['invoice'].number2, format2)
            sheet.write(row, 2, rec['invoice'].partner_id.name, format2)
            sheet.write(row, 3, rec['invoice'].partner_id.gst_number, format2)
            sheet.write(row, 4, rec['tax_5_sum'], format2)

            bill_total += rec['tax_5_sum']
            tax_5_total += rec['tax_5_sum']

            sheet.write(row, 5, rec['total_amount_cgst_5'], format2)

            bill_total += rec['total_amount_cgst_5']
            cgst_5 += rec['total_amount_cgst_5']

            sheet.write(row, 6, rec['total_amount_sgst_5'], format2)

            bill_total += rec['total_amount_sgst_5']
            igst_5 += rec['total_amount_sgst_5']

            sheet.write(row, 7, rec['tax_12_sum'], format2)

            bill_total += rec['tax_12_sum']
            tax_12_total += rec['tax_12_sum']

            sheet.write(row, 8, rec['total_amount_cgst_12'], format2)

            bill_total += rec['total_amount_cgst_12']
            cgst_12 += rec['total_amount_cgst_12']

            sheet.write(row, 9, rec['total_amount_sgst_12'], format2)

            bill_total += rec['total_amount_sgst_12']
            igst_12 += rec['total_amount_sgst_12']

            sheet.write(row, 10, rec['tax_18_sum'], format2)

            bill_total += rec['tax_18_sum']
            tax_18_total += rec['tax_18_sum']

            sheet.write(row, 11, rec['total_amount_cgst_18'], format2)

            bill_total += rec['total_amount_cgst_18']
            cgst_18 += rec['total_amount_cgst_18']

            sheet.write(row, 12, rec['total_amount_sgst_18'], format2)

            bill_total += rec['total_amount_sgst_18']
            igst_18 += rec['total_amount_sgst_18']

            sheet.write(row, 13, bill_total, format2)
            row += 1
            all_bill_total += bill_total
            bill_total = 0
        sheet.write(row+1, 0, "TOTAL", format3)
        sheet.write(row+1, 4, tax_5_total, format3)
        sheet.write(row+1, 5, cgst_5, format3)
        sheet.write(row+1, 6, igst_5, format3)
        sheet.write(row+1, 7, tax_12_total, format3)
        sheet.write(row+1, 8, cgst_12, format3)
        sheet.write(row+1, 9, igst_12, format3)
        sheet.write(row+1, 10, tax_18_total, format3)
        sheet.write(row+1, 11, cgst_18, format3)
        sheet.write(row+1, 12, igst_18, format3)
        sheet.write(row+1, 13, all_bill_total, format3)
BtobDateXlsx('report.pharmacy_mgmnt.b2b_hsn_tax_report_template_xlsx.xlsx', 'tax.report.wizard')