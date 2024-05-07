# import dateutil.utils
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

    pay_mode = fields.Selection([('cash', 'Cash'), ('credit', 'Credit'), ('upi', 'UPI')], 'Payment Mode')




