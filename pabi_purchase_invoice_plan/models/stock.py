# -*- coding: utf-8 -*-
import math
from openerp import models, fields, api, _
from openerp.exceptions import ValidationError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.multi
    def write(self, vals):
        """ Case invoice plane + asset only,
        write the unit price from WA to asset_value in stock_move """
        res = super(StockPicking, self).write(vals)
        if 'acceptance_id' in vals:
            acceptance_id = vals.get('acceptance_id', False)
            if acceptance_id:
                WA = self.env['purchase.work.acceptance']
                wa = WA.browse(acceptance_id)
                if wa.num_installment > 0:
                    asset_values = dict(
                        [(x.product_id.id, x.price_unit)
                         for x in wa.acceptance_line_ids]
                    )
                    for picking in self:
                        for move in picking.move_lines:
                            product = move.product_id
                            if move.product_id.asset:
                                move.asset_value = asset_values[product.id]
                            else:
                                move.asset_value = False
            else:  # Clear all asset_value
                for picking in self:
                    picking.move_lines.write({'asset_value': False})
        return res
