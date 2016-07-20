# -*- coding: utf-8 -*-

from openerp import models, api, fields, _
from openerp.exceptions import ValidationError


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    purchase_billing_id = fields.Many2one(
        'purchase.billing',
        string='Billing Number',
        readonly=True,
        copy=False,
    )
