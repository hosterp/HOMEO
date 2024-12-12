# import dateutil.utils
from lxml import etree
import json
from openerp.exceptions import except_orm, Warning, RedirectWarning, ValidationError


from num2words import num2words

from openerp import api, models, fields
from openerp.osv import osv
from openerp.tools.translate import _, _logger
from openerp.exceptions import except_orm, Warning, RedirectWarning, ValidationError
from datetime import datetime
from datetime import date
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import datetime

class AccountVoucher(models.Model):
    _inherit = 'account.voucher'

    pay_mode = fields.Selection([('credit', 'Credit'),('cash', 'Cash'),('upi', 'UPI'), ('card', 'Card'),('cheque','Cheque')], 'Payment Mode')
    res_person = fields.Many2one('res.partner', string="Responsible Person", domain=[('res_person_id', '=', True)])
    invoice_ids = fields.Many2many('account.invoice', string="Select Invoices", )
    amount_given=fields.Integer('Given Amount')
    balance=fields.Integer('Balance',compute='_compute_cash')

    @api.depends('amount_given')
    def _compute_cash(self):
        if self.amount_given:
            self.balance=self.amount_given-self.amount

    def onchange_amount(self, cr, uid, ids, amount, rate, partner_id, journal_id, currency_id, ttype, date,
                        payment_rate_currency_id, company_id, context=None):
        if not context:
            context = {}
        default = super(AccountVoucher, self).onchange_amount(cr, uid, ids, amount, rate, partner_id, journal_id,
                                                              currency_id, ttype, date, payment_rate_currency_id,
                                                              company_id, context=context)
        active_id = context.get('active_id')
        if active_id:
            cus_invoice = self.pool.get('account.invoice').browse(cr, uid, active_id, context=context)
            if cus_invoice:
                if amount < cus_invoice.residual and cus_invoice.type == 'out_invoice':
                    default['value'].update({'pay_mode': 'credit'})
                else:
                    default['value'].update({'pay_mode': cus_invoice.pay_mode})
        return default

    @api.multi
    def action_print_button(self):
        # Example: Call the print method from the account.invoice model
        invoice_ids = self.env['account.invoice'].search([('id', 'in', self.invoice_ids.ids)])
        return self.env['report'].get_action(invoice_ids, 'account.report_invoice')
    @api.onchange('pay_mode')
    def onchange_paymode(self):
        cus_invoice = self.env['account.invoice'].browse(self.env.context.get('active_id'))
        if self.pay_mode in ['credit', 'upi', 'card']:
            journal = self.env['account.journal'].search([('code', '=', 'BNK2')], limit=1)
            self.journal_id = journal.id
            self.account_id = journal.default_debit_account_id
        else:
            journal = self.env['account.journal'].search([('code', '=', 'BNK1')], limit=1)
            self.journal_id = journal.id
            self.account_id = journal.default_debit_account_id

        if self.amount < cus_invoice.residual and self.pay_mode != 'credit' and cus_invoice.type == 'out_invoice' :
            raise ValidationError(
                "Amount less than the invoice amount can only be paid through the Credit Payment Mode")


    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(AccountVoucher, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar,
                                                     submenu=submenu)
        if view_type == 'form':
            doc = etree.XML(res['arch'])
            for node in doc.xpath("//field[@name='res_person']"):
                modifiers = json.loads(node.get("modifiers", "{}"))
                modifiers['required'] = [('pay_mode', '=', 'credit')]
                node.set("modifiers", json.dumps(modifiers))
            res['arch'] = etree.tostring(doc, encoding='unicode')
        return res

    @api.multi
    def update_invoice_payment_details(self):
        self.ensure_one()
        cus_invoice = self.env['account.invoice'].browse(self.env.context.get('active_id'))
        if cus_invoice:
            if self.pay_mode == 'credit':
                if cus_invoice.pay_mode != self.pay_mode or (cus_invoice.res_person != self.res_person or False):
                    cus_invoice.pay_mode = self.pay_mode
                    cus_invoice.res_person = self.res_person
                else:
                    pass
            else:
                cus_invoice.pay_mode = self.pay_mode
                cus_invoice.res_person = self.res_person or False

    @api.multi
    def button_proforma_voucher(self):
        res = super(AccountVoucher, self).button_proforma_voucher()
        self.update_invoice_payment_details()
        return res


class AccountVoucherEntry(models.Model):
    _inherit = 'account.move'

    state = fields.Selection([('draft', 'Unposted'), ('posted', 'Posted'), ('cancel', 'Canceled')], )

