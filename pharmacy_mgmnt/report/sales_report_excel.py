try:
    from openerp.addons.report_xlsx.report.report_xlsx import ReportXlsx
except ImportError:
    class ReportXlsx(object):
        def __init__(self, *args, **kwargs):
            pass

class SalesReportXlsx(ReportXlsx):
    def generate_xlsx_report(self, workbook, data, lines):
        invoice_lines = lines.invoice_ids

        sheet = workbook.add_worksheet('Sales Report')

        bold = workbook.add_format({'bold': True})

        headers = ['Partner ', 'Invoice Date ', 'Number', 'Balance', 'Total', 'Status', 'Responsible Person']
        for col_num, header in enumerate(headers):
            sheet.write(0, col_num, header, bold)

        row = 1
        for line in invoice_lines:
            sheet.write(row, 0, line.partner_id.display_name)
            sheet.write(row, 1, line.date_invoice if line.date_invoice else '')
            sheet.write(row, 2, line.number2 if line.number2 else '')
            sheet.write(row, 3, line.residual)
            sheet.write(row, 4, line.amount_total)
            sheet.write(row, 5, line.state)
            sheet.write(row, 6, line.res_person.display_name if line.res_person else '')
            row += 1


SalesReportXlsx('report.pharmacy_mgmnt.sales_report_excel.xlsx', 'sales.report')
