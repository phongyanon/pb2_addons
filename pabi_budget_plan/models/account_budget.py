# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp.exceptions import ValidationError


class AccountBudget(models.Model):
    _inherit = 'account.budget'
    _order = 'create_date desc'

    policy_amount = fields.Float(
        string='Policy Amount',
        readonly=True,
    )

    @api.multi
    def _get_doc_number(self):
        self.ensure_one()
        _prefix = 'CTRL'
        _prefix2 = {'unit_base': 'UNIT',
                    'invest_asset': 'ASSET',
                    'project_base': 'PROJ',
                    'invest_construction': 'CONST',
                    'personnel': 'PERS'}
        _prefix3 = {'unit_base': 'section_id',
                    'invest_asset': 'org_id',
                    'project_base': 'program_id',
                    'invest_construction': 'org_id',
                    'personnel': 'personnel_costcenter_id'}
        prefix2 = _prefix2[self.chart_view]
        obj = self[_prefix3[self.chart_view]]
        prefix3 = obj.code or obj.name_short or obj.name
        name = '%s/%s/%s/%s' % (_prefix, prefix2,
                                self.fiscalyear_id.code, prefix3)
        return name

    @api.model
    def create(self, vals):
        budget = super(AccountBudget, self).create(vals)
        budget_level = budget.budget_level_id
        if budget_level.budget_release == 'manual_header' and \
                budget_level.release_follow_policy and \
                'policy_amount' in vals:
            vals['to_release_amount'] = vals['policy_amount']
            budget.write(vals)
        # Numbering
        budget.name = budget._get_doc_number()
        # --
        return budget

    @api.multi
    def write(self, vals):
        if 'policy_amount' in vals:
            for budget in self:
                budget_level = budget.budget_level_id
                if budget_level.budget_release == 'manual_header' and \
                        budget_level.release_follow_policy:
                    vals['to_release_amount'] = vals['policy_amount']
                super(AccountBudget, budget).write(vals)
        else:
            super(AccountBudget, self).write(vals)
        # Name
        for rec in self:
            if rec.name != rec._get_doc_number():
                rec._write({'name': rec._get_doc_number()})
        return True

    @api.multi
    @api.constrains('chart_view', 'fiscalyear_id', 'section_id', 'program_id',
                    'org_id', 'personnel_costcenter_id')
    def _check_fiscalyear_section_unique(self):
        for budget in self:
            budget = self.search(
                [('chart_view', '=', budget.chart_view),
                 ('fiscalyear_id', '=', budget.fiscalyear_id.id),
                 ('section_id', '=', budget.section_id.id),
                 ('program_id', '=', budget.program_id.id),
                 ('org_id', '=', budget.org_id.id),
                 ('personnel_costcenter_id', '=',
                  budget.personnel_costcenter_id.id),
                 ])
            if len(budget) > 1:
                raise ValidationError(
                    _('Duplicated budget on the same fiscal year!'))

    @api.multi
    def unlink(self):
        for policy in self:
            if policy.state not in ('draft', 'cancel'):
                raise ValidationError(
                    _('Cannot delete budget(s)\
                    which are not in draft or cancelled.'))
        return super(AccountBudget, self).unlink()
