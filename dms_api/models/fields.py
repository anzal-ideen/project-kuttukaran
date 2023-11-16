from odoo import api, fields, models
from datetime import datetime



class PaymentInherited(models.Model):
    _inherit = 'account.move'

    claim_from_date = fields.Date("Claim From Date")
    claim_to_date = fields.Date("Claim To Date")
