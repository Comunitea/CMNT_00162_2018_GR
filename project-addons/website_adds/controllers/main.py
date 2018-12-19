# -*- coding: utf-8 -*-
# © 2018 Comunitea
# Ruben Seijas <ruben@comunitea.com> - Pavel Smirnov <pavel@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, http, _
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.website_sale.models.sale_order import SaleOrder


class NewUpdateCart(WebsiteSale):

    @http.route(['/shop/cart/update'], type='http', auth="public", methods=['POST'], website=True, csrf=False)
    def cart_update(self, product_id, add_qty=1, set_qty=0, **kw):

        values = dict(request.env.context.copy())

        values.update({
            'start_date': kw['start_date'],
            'end_date': kw['end_date'],
            'number_of_days': kw['number_of_days'],
            'new_qty': add_qty,
        })

        request.env.context = values

        return super(NewUpdateCart, self).cart_update(product_id, add_qty=add_qty, set_qty=set_qty, **kw)


class NewSaleOrder(SaleOrder):

    @api.multi
    def _website_product_id_change(self, order_id, product_id, qty=0):
        order = self.sudo().browse(order_id)
        product_context = dict(self.env.context)
        product_context.setdefault('lang', order.partner_id.lang)
        product_context.update({
            'partner': order.partner_id.id,
            'quantity': qty,
            'date': order.date_order,
            'pricelist': order.pricelist_id.id,
        })
        product = self.env['product.product'].with_context(product_context).browse(product_id)
        pu = product.price
        if order.pricelist_id and order.partner_id:
            order_line = order._cart_find_product_line(product.id)
            if order_line:
                pu = self.env['account.tax']._fix_tax_included_price_company(pu, product.taxes_id,
                                                                             order_line[0].tax_id, self.company_id)
                # qty = qty - order_line.product_uom_qty

        return {
            'product_id': product_id,
            'product_uom_qty': product_context['new_qty'],
            'order_id': order_id,
            'product_uom': product.uom_id.id,
            'price_unit': pu,
            'start_date': product_context['start_date'],
            'end_date': product_context['end_date'],
            'number_of_days': product_context['number_of_days'],
        }
