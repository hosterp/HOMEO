from openerp.exceptions import Warning as UserError
from openerp import models, fields, api, _
from openerp.osv.fields import datetime


class CashBook(models.Model):
	_name = 'cash.book'
	_rec_name = 'id'
	_order = 'id desc'

	move_id = fields.Many2one('account.move')
	period_id = fields.Many2one('account.period')
	date_from = fields.Date('Date From', default=fields.date.today())
	date_to = fields.Date('Date To', default=fields.date.today())
	cash_book_ids = fields.One2many('cash.book.line', 'cash_book_id', 'Transactions')
	# total_debit = fields.Float("Total", compute="_compute_total_debit",)
	# total_credit = fields.Float("Credited", compute="_compute_total_debit",)
	total_balance = fields.Float("Balance", compute="_compute_total_debit",)
	pay_mode = fields.Selection([('cash', 'Cash'), ('credit', 'Credit'), ('upi', 'UPI')], 'Payment Mode')

	@api.depends('cash_book_ids.amount')
	def _compute_total_debit(self):
		for record in self:
			total_balance = sum(line.amount for line in record.cash_book_ids)
			record.total_balance = total_balance

	@api.multi
	def view_collection(self):
		domain = [('date_invoice', '>=', self.date_from), ('date_invoice', '<=', self.date_to or fields.Date.today()),('state','!=','cancel'),('state','=','paid')]
		if self.pay_mode:
			domain.append(('pay_mode', '=', self.pay_mode))
		datas = self.env['account.invoice'].search(domain)
		line_records=[]
		for rec in datas:
			# if rec.line_ids:
			# 	for line in rec.line_ids:
					if rec.amount_total != 0:
						line_records.append((0, 0, {
							"invoice": rec.number2,
							"partner_id": rec.partner_id.id,
							"amount": rec.amount_total,
							"journal_id": rec.journal_id.id,
							"pay_mode": rec.pay_mode,
							"validated_by": rec.validated_by_user,
						}))

		payment_domain = [
			('date', '>=', self.date_from),
			('date', '<=', self.date_to or fields.Date.today()),
			('state', '!=', 'cancel')
		]

		if self.pay_mode:
			payment_domain.append(('payment_method', '=', self.pay_mode))
		payments = self.env['partner.payment'].search(payment_domain)
		for payment in payments:
			if payment.amount != 0:
					# if payment.invoice_ids:
					# 	for rec in payment.invoice_ids:
					# 		if rec.select != True:
								line_records.append((0, 0, {
									"invoice": payment.reference_number,
									"partner_id": payment.partner_id.id if payment.partner_id else False,
									"amount": payment.payment_amount,
									"journal_id": payment.journal_id.id if payment.journal_id else False,
									"pay_mode": payment.payment_method,
									"validated_by": payment.validated_by_user,
								}))
		if self.cash_book_ids:
			self.cash_book_ids = [(5, 0, 0)]
			self.cash_book_ids = line_records
		else:
			self.cash_book_ids = line_records


class CashBookLines(models.Model):
	_name = "cash.book.line"

	cash_book_id = fields.Many2one('cash.book', 'CashBook')
	Journal_id = fields.Many2one('account.voucher','Invoice')
	partner_id = fields.Many2one('res.partner','Partner')
	amount = fields.Float("Amount")
	invoice = fields.Char('Invoice')
	validated_by = fields.Char('Validated By')
	pay_mode = fields.Selection([('cash', 'Cash'), ('credit', 'Credit'), ('upi', 'UPI'),('cheque', 'Cheque'),('card','Card')], 'Payment Mode')






