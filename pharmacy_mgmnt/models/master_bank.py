from datetime import datetime, timedelta
from datetime import timedelta
import openerp.addons.decimal_precision as dp
from openerp.exceptions import except_orm, Warning, RedirectWarning


# import models
from dateutil.relativedelta import relativedelta

from openerp import models, fields, api, tools, _


class BankAccounts(models.Model):
    _name = 'master.bank'

    name = fields.Char('Bank Name', required=False, copy=False)
    account_number = fields.Integer('Account No', required=False, copy=False)
    ifsc_number = fields.Char('IFSC No', required=False, copy=False)
    branch = fields.Char('Branch', required=False, copy=False)
