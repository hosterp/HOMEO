from collections import defaultdict
from datetime import datetime

try:
    from openerp.addons.report_xlsx.report.report_xlsx import ReportXlsx
except ImportError:
    class ReportXlsx(object):
        def __init__(self, *args, **kwargs):
            pass

class BtocDateXlsx(ReportXlsx):
    def generate_xlsx_report(self, workbook, data, lines):
        if lines.b2c:
            if lines.type == 'interstate':
                partner_ids = self.env['res.partner'].search([
                    ('b2c', '=', True), ('interstate_customer', '=', True)])
            elif lines.type == 'local':
                partner_ids = self.env['res.partner'].search([
                    ('b2c', '=', True), ('interstate_customer', '=', False)])
            else:
                partner_ids = self.env['res.partner'].search([
                    ('b2c', '=', True)])
            # partner_ids = self.env['res.partner'].search([
            #     ('b2c', '=', True), ('b2b', '=', False)])

            invoices = self.env['account.invoice'].search(
                [("date_invoice", ">=", lines.from_date), ("date_invoice", "<=", lines.to_date),
                 ('partner_id.customer', '=', True), ('partner_id', 'in', partner_ids.ids),
                 ('packing_slip', '=', False), ('holding_invoice', '=', False),
                 ('type', '=', 'out_invoice'), ('state', '=', 'paid')])

            merged_data = defaultdict(lambda: {
                'tax_5_sum': 0,
                'tax_12_sum': 0,
                'tax_18_sum': 0,
                'total_amount_sgst_5': 0,
                'total_amount_sgst_12': 0,
                'total_amount_sgst_18': 0,
                'total_amount_cgst_5': 0,
                'total_amount_cgst_12': 0,
                'total_amount_cgst_18': 0,
                'invoice_numbers': [],
            })

            for invoice in invoices:
                date_str = invoice.date_invoice  # Assuming date_invoice is a string
                date = datetime.strptime(date_str, '%Y-%m-%d').date()

                tax_5 = invoice.invoice_line.filtered(lambda l: l.invoice_line_tax_id4 == 5)
                tax_12 = invoice.invoice_line.filtered(lambda l: l.invoice_line_tax_id4 == 12)
                tax_18 = invoice.invoice_line.filtered(lambda l: l.invoice_line_tax_id4 == 18)

                tax_5_sum = sum(tax_5.mapped('amt_w_tax'))
                tax_12_sum = sum(tax_12.mapped('amt_w_tax'))
                tax_18_sum = sum(tax_18.mapped('amt_w_tax'))

                # Accumulate values in the dictionary
                merged_data[date]['invoice_numbers'].append(invoice.number2)
                merged_data[date]['tax_5_sum'] += tax_5_sum
                merged_data[date]['tax_12_sum'] += tax_12_sum
                merged_data[date]['tax_18_sum'] += tax_18_sum

                merged_data[date]['total_amount_sgst_5'] += (tax_5_sum * 0.05) / 2
                merged_data[date]['total_amount_sgst_12'] += (tax_12_sum * 0.12) / 2
                merged_data[date]['total_amount_sgst_18'] += (tax_18_sum * 0.18) / 2

                merged_data[date]['total_amount_cgst_5'] += (tax_5_sum * 0.05) / 2
                merged_data[date]['total_amount_cgst_12'] += (tax_12_sum * 0.12) / 2
                merged_data[date]['total_amount_cgst_18'] += (tax_18_sum * 0.18) / 2

            # Convert the merged data back to a list
            data_list = []
            for date, values in merged_data.items():
                data_list.append({
                    # 'date': date,
                    'date': date.strftime('%d-%m-%Y'),
                    'tax_5_sum': values['tax_5_sum'],
                    'tax_12_sum': values['tax_12_sum'],
                    'tax_18_sum': values['tax_18_sum'],
                    'total_amount_sgst_5': values['total_amount_sgst_5'],
                    'total_amount_sgst_12': values['total_amount_sgst_12'],
                    'total_amount_sgst_18': values['total_amount_sgst_18'],
                    'total_amount_cgst_5': values['total_amount_cgst_5'],
                    'total_amount_cgst_12': values['total_amount_cgst_12'],
                    'total_amount_cgst_18': values['total_amount_cgst_18'],
                    'first_invoice_number': values['invoice_numbers'][0] if values['invoice_numbers'] else None,
                    'last_invoice_number': values['invoice_numbers'][-1] if values['invoice_numbers'] else None,
                })
                for entry in data_list:
                    date = entry['date']
                    invoice_numbers = merged_data[date]['invoice_numbers']
                    entry['invoice_numbers'] = invoice_numbers
                # print(data_list,'data')
            format = workbook.add_format({'font_size': 14, 'align': 'vcentre', 'bold': True})
            format1 = workbook.add_format({'font_size': 10, 'align': 'vcentre', 'bold': True})
            format2 = workbook.add_format({'font_size': 8, 'align': 'vcentre', 'bold': False})
            format3 = workbook.add_format({'font_size': 9, 'align': 'vcentre', 'bold': True})
            sheet = workbook.add_worksheet('b2c by date wise')
            sheet.write(2, 4, "TRAVANCORE HOMEO-GST TAX REPORT", format)
            from_date_str = lines.from_date
            to_date_str = lines.to_date
            from_date = datetime.strptime(from_date_str, '%Y-%m-%d')
            to_date = datetime.strptime(to_date_str, '%Y-%m-%d')
            formatted_from_date = from_date.strftime('%d-%m-%Y')
            formatted_to_date = to_date.strftime('%d-%m-%Y')
            sheet.write(3, 3, "BTOC TAX REPORT BY BILL WISE {} - {}".format(formatted_from_date, formatted_to_date),
                        format)

            # sheet.write(3, 4, "BTOC TAX REPORT BY BILL WISE", format)

            sheet.write(5, 0, "DATE", format1)
            sheet.write(5, 1, "Sales5%", format1)
            sheet.write(5, 2, "CGST", format1)
            sheet.write(5, 3, "IGST", format1)
            sheet.write(5, 4, "Sales12%", format1)
            sheet.write(5, 5, "CGST", format1)
            sheet.write(5, 6, "IGST", format1)
            sheet.write(5, 7, "Sales18%", format1)
            sheet.write(5, 8, "CGST", format1)
            sheet.write(5, 9, "IGST", format1)
            sheet.write(5, 10, "Bill AMOUNT", format1)
            sheet.write(5, 11, "Bill No", format1)
            row = 6

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
                bill_total = 0
                # print(rec,'rec')
                sheet.write(row, 0, rec['date'], format2)
                sheet.write(row, 1, rec.get('tax_5_sum'), format2)

                bill_total += rec.get('tax_5_sum')
                tax_5_total +=rec.get('tax_5_sum')
                bill_total += rec['total_amount_cgst_5']
                cgst_5 += rec['total_amount_cgst_5']
                bill_total += rec['total_amount_sgst_5']
                igst_5 += rec['total_amount_sgst_5']

                bill_total += rec['tax_12_sum']
                tax_12_total += rec['tax_12_sum']
                bill_total += rec['total_amount_cgst_12']
                cgst_12 += rec['total_amount_cgst_12']
                bill_total += rec['total_amount_sgst_12']
                igst_12 += rec['total_amount_sgst_12']

                bill_total += rec['tax_18_sum']
                tax_18_total += rec['tax_18_sum']
                bill_total += rec['total_amount_cgst_18']
                cgst_18 += rec['total_amount_cgst_18']
                bill_total += rec['total_amount_sgst_18']
                igst_18 += rec['total_amount_sgst_18']

                sheet.write(row, 2, rec.get('total_amount_cgst_5'), format2)
                sheet.write(row, 3, rec.get('total_amount_sgst_5'), format2)
                sheet.write(row, 4, rec.get('tax_12_sum'), format2)
                sheet.write(row, 5, rec.get('total_amount_cgst_12'), format2)
                sheet.write(row, 6, rec.get('total_amount_sgst_12'), format2)
                sheet.write(row, 7, rec.get('tax_18_sum'), format2)
                sheet.write(row, 8, rec.get('total_amount_cgst_18'), format2)
                sheet.write(row, 9, rec.get('total_amount_sgst_18'), format2)
                combined_invoice_numbers = "{} - {}".format(rec.get('first_invoice_number', '~'),
                                                           rec.get('last_invoice_number', '~'))
                sheet.write(row, 11, combined_invoice_numbers, format2)
                sheet.write(row, 10, bill_total, format2)

                all_bill_total += bill_total
                row += 1
            sheet.write(row+1, 10, all_bill_total, format3)
            bill_total = 0
        sheet.write(row + 1, 0, "TOTAL", format3)
        sheet.write(row + 1, 1, tax_5_total, format3)
        sheet.write(row + 1, 2, cgst_5, format3)
        sheet.write(row + 1, 3, igst_5, format3)
        sheet.write(row + 1, 4, tax_12_total, format3)
        sheet.write(row + 1, 5, cgst_12, format3)
        sheet.write(row + 1, 6, igst_12, format3)
        sheet.write(row + 1, 7, tax_18_total, format3)
        sheet.write(row + 1, 8, cgst_18, format3)
        sheet.write(row + 1, 9, igst_18, format3)
        # sheet.write(row + 1, 10, bill_total, format3)
BtocDateXlsx('report.pharmacy_mgmnt.b2c_tax_report_template_xlsx.xlsx', 'tax.report.wizard')