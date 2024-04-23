from openerp.exceptions import Warning as UserError
from openerp import models, fields, api, _
from openerp.osv.fields import datetime
from datetime import datetime



class ExpenseBook(models.Model):
	_name = 'expense.book'
	_rec_name = 'date'
	_order = 'id desc'

	period_id = fields.Many2one('account.period', string="Period", readonly=True,
								default=lambda self: self.get_current_period().id)
	date = fields.Date('Date', default=fields.date.today(), readonly=True)
	expense_book_ids = fields.One2many('expense.book.line', 'expense_book_id', 'Transactions')
	total_debit = fields.Float("Total", compute="_compute_total_debit",)
	total_credit = fields.Float("Credited", compute="_compute_total_debit",)
	total_balance = fields.Float("Balance", compute="_compute_total_debit",)
	status = fields.Selection([('balanced','Balanced'),('unbalanced','Unbalanced')],default='unbalanced',compute="_compute_status",)

	@api.depends('expense_book_ids.status')
	def _compute_status(self):
		for record in self:
			unbalanced = any(line.status != 'balanced' for line in record.expense_book_ids)
			record.status = 'unbalanced' if unbalanced else 'balanced'

	def get_current_period(self):
		current_date = datetime.now().date()
		current_period = self.env['account.period'].search(
			[('date_start', '<=', current_date), ('date_stop', '>=', current_date)], limit=1)
		return current_period

	@api.depends('expense_book_ids.debit','expense_book_ids.credit','expense_book_ids.balance')
	def _compute_total_debit(self):
		for record in self:
			total_debit = sum(line.debit for line in record.expense_book_ids)
			record.total_debit = total_debit
			total_credit = sum(line.credit for line in record.expense_book_ids)
			record.total_credit = total_credit
			total_balance = sum(line.balance for line in record.expense_book_ids)
			record.total_balance = total_balance


class CashBookLines(models.Model):
	_name = "expense.book.line"
	# _inherits = {'account.move.line': 'move_id'}

	expense_book_id = fields.Many2one('expense.book', 'ExpenseBook')
	journal_id = fields.Many2one('account.journal', default=7, string='Journal')
	account_id = fields.Many2one("account.account", string='Account',
								 default=23)
	expense_type_id = fields.Many2one('expense.types',required=True)
	debit = fields.Float("Debit")
	credit = fields.Float("Credit")
	balance = fields.Float("Balance")
	narration = fields.Text("Narration")
	status = fields.Selection([('balanced','Balanced'),('unbalanced','Unbalanced')],default='unbalanced')



	@api.onchange('credit')
	def credit_onchange(self):
		if self.credit:
			self.balance = self.debit - self.credit
			if self.balance == 0:
				self.status = 'balanced'
			else:
				self.status = 'unbalanced'
		else:
			self.balance = self.debit
			self.status = 'unbalanced'

class ExpenseTypes(models.Model):
	_name = "expense.types"

	name = fields.Char('Name')

