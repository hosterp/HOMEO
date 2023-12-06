from datetime import datetime

try:
    from openerp.addons.report_xlsx.report.report_xlsx import ReportXlsx
except ImportError:
    class ReportXlsx(object):
        def __init__(self, *args, **kwargs):
            pass

class EnquiryXlsx(ReportXlsx):
    def generate_xlsx_report(self, workbook, data, lines):
        format = workbook.add_format({'font_size': 14, 'align': 'vcentre', 'bold': True})
        format1 = workbook.add_format({'font_size': 10, 'align': 'vcentre', 'bold': True})
        format2 = workbook.add_format({'font_size': 12, 'align': 'vcentre', 'bold': False})
        format3 = workbook.add_format({'font_size': 13, 'align': 'vcentre', 'bold': True})
        format4 = workbook.add_format({'font_size':8,'align':'vcentre','bold':False})

        sheet = workbook.add_worksheet('enquiry')
        sheet.merge_range('F3:L3', "TRAVANCORE HOMEO MEDICALS", format)
        # sheet.write(3, 6, "TC 25/1613(1) SS KOVIL ROAD THAMPANOOR", format1)
        # sheet.write(4, 3, "TRIVANDRUM - 695001, KERALA-32,PH:0471-4010102,2335863 and travancorehomeo@gmail.com", format2)
        # sheet.write(5, 4, "GSTIN : 32AYAPS1856Q1ZY , DLNO:TVM-111350,TVM-111351 [20C 20D]", format3)
        sheet.merge_range('G4:I4', "ORDER"+" " + datetime.strftime(datetime.strptime (lines.date, "%Y-%m-%d"), "%d-%m-%Y"), format3)

        sheet.write(6, 5, "Medicine ", format1)
        sheet.write(6, 6, "Potency  ", format1)
        sheet.write(6, 7, "Packing   ", format1)
        sheet.write(6, 8, "Quantity   ", format1)

        row =7
        record = self.env['medicine.enquiry'].search([('medicine_ids', 'in', [lines.id])])
        for rec in record:
            # sheet.write(3,8,rec.date,format3)
            for line in rec.medicine_ids:
                sheet.write(row, 5, line.medicine_id.name, format4)
                sheet.write(row, 6,  line.potency_id.display_name, format4)
                sheet.write(row, 7,  line.packing_id.display_name, format4)
                sheet.write(row, 8,  line.qty, format4)
                row += 1
            # sheet.write(row, 6, rec['medicine_line_id'].medicine_id, format2)

EnquiryXlsx('report.pharmacy_mgmnt.enquiry_report_xlsx.xlsx', 'medicine.enquiry')