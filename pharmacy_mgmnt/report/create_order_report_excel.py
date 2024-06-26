try:
    from openerp.addons.report_xlsx.report.report_xlsx import ReportXlsx
except ImportError:
    class ReportXlsx(object):
        def __init__(self, *args, **kwargs):
            pass

class CreateorderReportXlsx(ReportXlsx):
    def generate_xlsx_report(self, workbook, data, lines):
        format = workbook.add_format({'font_size': 14, 'align': 'vcentre', 'bold': True})
        format1 = workbook.add_format({'font_size': 10, 'align': 'vcentre', 'bold': True})
        format2 = workbook.add_format({'font_size': 12, 'align': 'vcentre', 'bold': False})
        format3 = workbook.add_format({'font_size': 13, 'align': 'vcentre', 'bold': True})
        format4 = workbook.add_format({'font_size': 8, 'align': 'vcentre', 'bold': False})

        sheet = workbook.add_worksheet('enquiry')
        sheet.merge_range('F3:L3', "TRAVANCORE HOMEO MEDICALS", format)
        sheet.merge_range('G4:H4', "Stock Order", format)

        sheet.write(6, 5, "Medicine ", format1)
        sheet.write(6, 6, "Packing ", format1)
        sheet.write(6, 7, "Potency ", format1)
        sheet.write(6, 8, "	Company ", format1)
        sheet.write(6, 9, "	New Order  ", format1)


        if lines.stock_view_ids:
            new_lines = []
            for rec in lines.stock_view_ids:
                if rec.number_of_order != 0:
                    new_lines.append((0, 0, {

                        'medicine_id': rec.medicine_id.id,
                        'rack': rec.rack.id,
                        'potency': rec.potency.id,
                        'company': rec.company.id,
                        'medicine_name_packing': rec.medicine_name_packing.id,
                        'medicine_grp1': rec.medicine_grp1.id,
                        'qty': rec.qty,
                        'mrp': rec.mrp,
                        'batch_2': rec.batch_2,
                        'manf_date': rec.manf_date,
                        'expiry_date': rec.expiry_date,
                        'new_order': rec.number_of_order,
                    }))
                    # self.write({'order_ids': new_lines})
                    rec.number_of_order = 0
                    lines.order_ids = new_lines

            row = 7
            for order in lines.order_ids:
                sheet.write(row, 5, order.medicine_id.display_name, format4)
                sheet.write(row, 6, order.medicine_name_packing.display_name, format4)
                sheet.write(row, 7, order.potency.display_name, format4)
                sheet.write(row, 8, order.company.display_name, format4)
                sheet.write(row, 9, order.new_order, format4)
                row += 1

CreateorderReportXlsx('report.pharmacy_mgmnt.print_create_order_report_xlsx.xlsx', 'create.order')