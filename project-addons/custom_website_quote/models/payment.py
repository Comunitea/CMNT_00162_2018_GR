# -*- coding: utf-8 -*-
# © 2019 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, models, fields


class PaymentAcquirer(models.Model):

    _inherit = 'payment.acquirer'

    quote_available = fields.Boolean()

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        res = super(PaymentAcquirer, self).search(
            args, offset, limit, order, count)
        if self._context.get('quote_payments'):
            res = res.filtered(lambda r: not r.charge_fee and r.quote_available)
        if self._context.get('order_price'):
            filter_price = self.env['sale.order'].browse(
                self._context.get('order_price')).amount_total
            res = res.filtered(
                lambda r: (not r.min_amount_required and not r.max_amount_required) or
                ((r.min_amount_required < filter_price and r.max_amount_required > filter_price) or
                    (not r.max_amount_required and r.min_amount_required < filter_price) or
                    (not r.min_amount_required and r.max_amount_required > filter_price)))
        return res
