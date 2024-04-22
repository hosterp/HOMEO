from openerp.exceptions import Warning as UserError
from openerp import models, fields, api, _
from openerp.osv.fields import datetime


class CashBook(models.Model):
	_name = 'cash.book'
	_rec_name = 'date'
	_order = 'date desc'

	move_id = fields.Many2one('account.move')
	period_id = fields.Many2one('account.period')
	date = fields.Date('Date', default=fields.date.today())
	cash_book_ids = fields.One2many('cash.book.line', 'cash_book_id', 'Transactions')


	@api.multi
	def view_collection(self):
		datas = self.env['account.move'].search([('date','=',self.date),('line_id.credit','!=',0)])
		line_record = []
		for rec in datas:
			if rec.line_id:
				for lines in rec.line_id:
					if lines.credit != 0:
						line_record.append((0, 0,{
							"name": lines.name,
							"invoice": lines.invoice.id,
							"partner_id":lines.partner_id.id,
							"debit":lines.debit,
							"credit":lines.credit,
							"account_id":lines.account_id.id,
							"journal_id":lines.move_id.journal_id.id,
							"amount_residual":lines.amount_residual,
						}))
		if self.cash_book_ids:
			self.cash_book_ids = [(5, 0, 0)]
			self.cash_book_ids = line_record
		else:
			self.cash_book_ids = line_record


class CashBookLines(models.Model):
	_name = "cash.book.line"
	_inherits = {'account.move.line': 'move_id'}

	move_line_id = fields.Many2one('account.move.line', )
	cash_book_id = fields.Many2one('cash.book', 'CashBook')



