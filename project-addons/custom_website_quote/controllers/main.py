# -*- coding: utf-8 -*-
# © 2019 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import http
from odoo.http import request
from odoo.addons.website_quote.controllers.main import sale_quote


class SaleQuoteCustom(sale_quote):

    @http.route("/quote/<int:order_id>/<token>", type='http', auth="public", website=True)
    def view(self, order_id, pdf=None, token=None, message=False, **post):
        new_ctxt = dict(request.env.context)
        new_ctxt.update({'quote_payments': True, 'order_price': order_id})
        request.env.context = new_ctxt
        res = super(SaleQuoteCustom, self).view(order_id, pdf, token, message, **post)
        return res

    @http.route(['/quote/<int:order_id>/transaction/<int:acquirer_id>/<token>'], type='json', auth="public", website=True)
    def payment_transaction_token(self, acquirer_id, order_id, token):
        request.session['sale_last_order_id'] = order_id
        return super(SaleQuoteCustom, self).payment_transaction_token(acquirer_id, order_id, token)
