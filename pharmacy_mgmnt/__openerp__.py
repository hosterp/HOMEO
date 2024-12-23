# -*- coding: utf-8 -*-
##############################################################################

##############################################################################
{
    'name': "Pharmacy Management",
    'version': '10.0.1.1.1',
    'summary': """Pharmacy Management and Customer/Supplier Invoice""",
    'description': """This Module for Pharmacy Management and it Enables To Create Stocks Picking From Customer/Supplier Invoice""",
    'author': "Hiworth Solutions",
    'company': 'Hiworth Solutions',
    'website': "https://www.hiworthsolutions.com",
    'category': 'Accounting',
    'depends': ['base', 'account', 'stock', 'purchase', 'sale', 'report',
                'report_xlsx', 'report_custom_filename',
                'account_accountant', 'product_expiry', 'product_expiry_simple', 'Key_shortcuts', 'account_cancel'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/account_invoice_view_wizard.xml',
        'views/res_partner_views.xml',
        'views/menu.xml',
        'views/rack_transfer.xml',
        'views/partial_transfer.xml',
        'views/credit_limit.xml',
        'views/invoice_history.xml',
        'views/invoice_stock_move_view.xml',
        'views/product.xml',
        'views/invoice.xml',
        'views/stockpicking.xml',
        'views/master_menu.xml',
        'views/enquiry.xml',
        'views/stock_view_and_order.xml',
        'expiry_manage/expiry_manage_view.xml',
        'report/customer_inv_report.xml',
        'report/supplier_inv_report.xml',
        'report/pending_invoice_report.xml',
        'report/customer_inv_history.xml',
        'report/supplier_inv_history.xml',
        'report/purchase_report.xml',
        'report/tax_report_excel_to_pdf.xml',
        'report/customer_payment_report.xml',
        'report/enquiry_report.xml',
        'report/stock_order_report.xml',

        'report/inherit_supplier_invoice_report.xml',
        'report/e_way_report_customer.xml',
        'report/payment_history_invoice_line_report.xml',

        'report/packing_holding_history.xml',
        'report/tax_report_view.xml',
        'report/tax_report_excel.xml',
        'report/tax_b2c_hsn.xml',
        'report/sales_report.xml',
        'report/sale_report.xml',
        'report/create_order_report.xml',
        'views/account_invoice_view.xml',
        'views/invoice_report.xml',
        'views/master_bank.xml',
        'views/credit_payment_view.xml',
        'views/cash_and_expense_book.xml',
        'views/expense_book.xml',
        'views/template.xml',
        'views/account_voucher.xml',
        'views/custom_refunds_views.xml',
        'views/custom_supplier_refunds_views.xml',
        'views/create_order.xml',
        'views/supplier_wizard_form.xml',
        'views/home_page.xml',
        'views/quotation.xml',
        'views/stock_search.xml',
        'views/quotation_default.xml',
        'views/password_authentication.xml',
        'views/payment_page_password_validation.xml',
        'views/supplier_page_password_validation.xml',
        # 'views/view_port.xml',


    ],
    'js': [
        "static/src/js/widget.js",
        "static/src/js/cursor_movement.js",
    ],
    'qweb': [
        "static/src/xml/save_and_create_button.xml",
    ],
    'images': ['static/description/banner.jpg'],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
}
