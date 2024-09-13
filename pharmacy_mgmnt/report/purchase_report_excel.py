try:
    from openerp.addons.report_xlsx.report.report_xlsx import ReportXlsx
except ImportError:
    class ReportXlsx(object):
        def __init__(self, *args, **kwargs):
            pass

class PurchaseReportXlsx(ReportXlsx):
    def generate_xlsx_report(self, workbook, data, lines):

        invoice_lines = lines.get_details()


        sheet = workbook.add_worksheet('Purchase Invoice Report')


        bold = workbook.add_format({'bold': True})


        headers = ['Date', 'Bill No', 'Product', 'Batch', 'Expiry', 'Rack', 'Purchased Qty']
        for col_num, header in enumerate(headers):
            sheet.write(0, col_num, header, bold)


        row = 1
        for line in invoice_lines:
            sheet.write(row, 0, line.invoice_id.date_invoice)
            sheet.write(row, 1, line.invoice_id.number2 if line.invoice_id.number2 else '')
            sheet.write(row, 2, line.product_id.name if line.product_id else '')
            sheet.write(row, 3, line.batch_2.batch if line.batch_2.batch else '')
            sheet.write(row, 4, line.expiry_date if line.expiry_date else '')
            sheet.write(row, 5, line.medicine_rack.medicine_type)
            sheet.write(row, 6, line.quantity)
            row += 1


PurchaseReportXlsx('report.pharmacy_mgmnt.purchase_report_excel.xlsx', 'purchase.invoice.report')
