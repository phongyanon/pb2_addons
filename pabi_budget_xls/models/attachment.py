# -*- coding: utf-8 -*-
from openerp import models, fields


class Attachment(models.Model):
    _inherit = 'ir.attachment'

    budget_template = fields.Boolean('Budget Template')
    budget_plan_id = fields.Many2one(
        'budget.plan.unit',
        string="Budget Plan",
        copy=False,
    )

    def init(self, cr):
        if 'budget.plan.unit' not in self._models_check:
            self._models_check.update({'budget.plan.unit': 'budget_plan_id'})
