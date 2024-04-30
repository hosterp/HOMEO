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

	@api.depends('cash_book_ids.amount')
	def _compute_total_debit(self):
		for record in self:
			total_balance = sum(line.amount for line in record.cash_book_ids)
			record.total_balance = total_balance


	@api.multi
	def view_collection(self):
		datas = self.env['account.voucher'].search([('date', '>=', self.date_from), ('date', '<=', self.date_to or datetime.date.today())])

		print(datas,'datas')
		line_record = []
		for rec in datas:
			if rec.line_ids:
				for lines in rec.line_ids:
					if lines.amount != 0:
						line_record.append((0, 0,{
							"invoice": rec.reference,
							"partner_id":rec.partner_id.id,
							"amount":lines.amount,
							"journal_id":rec.journal_id.id,
						}))
		if self.cash_book_ids:
			self.cash_book_ids = [(5, 0, 0)]
			self.cash_book_ids = line_record
		else:
			self.cash_book_ids = line_record


class CashBookLines(models.Model):
	_name = "cash.book.line"
	# _inherits = {'account.voucher.line': 'voucher_id'}
	#
	# voucher_line_id = fields.Many2one('account.voucher.line', )
	cash_book_id = fields.Many2one('cash.book', 'CashBook')
	Journal_id = fields.Many2one('account.voucher','Invoice')
	partner_id = fields.Many2one('res.partner','Partner')
	amount = fields.Float("Amount")
	invoice = fields.Char('Invoice')





