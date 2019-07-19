# -*- coding: utf-8 -*-

from odoo import api, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    def _website_product_id_change(self, order_id, product_id, qty=0):
        """
        Add dates and days to context
        """
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