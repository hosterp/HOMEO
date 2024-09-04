import datetime

from pychart.line_style import default

from openerp import models, fields, api
from openerp.fields import Datetime


class StockSearchExpiry(models.Model):
    _name = 'search.stock.expiry'

    type = fields.Selection([('30', '30'), ('60', '60'), ('90', '90'), ('120', '120')])
    stock_ids=fields.One2many('entry.stock','expiry_id')

    @api.onchange('type')
    def _get_values(self):
        if self.type:
            days = int(self.type)
            print(days,'days')
            today = datetime.date.today()
            target_date = today + datetime.timedelta(days=days)
            print(target_date,'target_date')
            domain = []

            if self.type == '30':
                domain=[('expiry_date', '<=', target_date)]

            elif self.type == '60':
                domain=[('expiry_date', '<=', target_date)]

            elif self.type == '90':
                domain=[('expiry_date', '<=', target_date)]

            elif self.type == '120':
                domain = [('expiry_date', '<=', target_date)]

            else:
                pass

            records = self.env['entry.stock'].search(domain)
            self.stock_ids = [(6, 0, records.ids)]
        else:
            records = self.env['entry.stock'].search([])
            self.stock_ids = [(6, 0, records.ids)]
