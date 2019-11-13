# -*- coding: utf-8 -*-

from odoo import http

from odoo.http import request

from odoo.addons.website_sale.controllers.main import WebsiteSale


class NewUpdateCart(WebsiteSale):

    @http.route(['/shop/cart/update'], type='http', auth="public", methods=['POST'], website=True, csrf=False)
    def cart_update(self, product_id, add_qty=1, set_qty=0, **kw):
        # Only one product in cart
        sale_order = request.website.sale_get_order(force_create=True)
        if sale_order:
            # unlink order_line.
            order_line = request.env['sale.order.line'].sudo().search([('order_id', '=', sale_order.id)])
            if order_line:
                order_line.unlink()
        # Update context with new rental values
        values = dict(request.env.context.copy())
        values.update({
            'start_date': kw['start_date'],
            'end_date': kw['end_date'],
            'number_of_days': kw['number_of_days'],
            'new_qty': add_qty,
        })
        request.env.context = values
        return super(NewUpdateCart, self).cart_update(product_id, add_qty=add_qty, set_qty=set_qty, **kw)

