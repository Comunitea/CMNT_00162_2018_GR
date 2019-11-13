# -*- coding: utf-8 -*-
import logging

from odoo import api, models
from odoo.http import request
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    def _cart_update(self, product_id=None, line_id=None, add_qty=0, set_qty=0, attributes=None, **kwargs):
        """
            Add or set product quantity, add_qty can be negative

            Hook to change product template by rental service, including price_unit by pricelist items
        """
        self.ensure_one()
        SaleOrderLineSudo = self.env['sale.order.line'].sudo()

        try:
            if add_qty:
                add_qty = float(add_qty)
        except ValueError:
            add_qty = 1
        try:
            if set_qty:
                set_qty = float(set_qty)
        except ValueError:
            set_qty = 0
        quantity = 0
        order_line = False
        if self.state != 'draft':
            request.session['sale_order_id'] = None
            raise UserError(_('It is forbidden to modify a sale order which is not in draft status'))
        if line_id is not None:
            order_lines = self._cart_find_product_line(product_id, line_id, **kwargs)
            order_line = order_lines and order_lines[0]

        # Create line if no line with product_id can be located
        if not order_line:
            values = self._website_product_id_change(self.id, product_id, qty=1)
            values['name'] = self._get_line_description(self.id, product_id, attributes=attributes)
            order_line = SaleOrderLineSudo.create(values)

            try:
                order_line._compute_tax_id()
            except ValidationError as e:
                # The validation may occur in backend (eg: taxcloud) but should fail silently in frontend
                _logger.debug("ValidationError occurs during tax compute. %s" % (e))
            if add_qty:
                add_qty -= 1

        # compute new quantity
        if set_qty:
            quantity = set_qty
        elif add_qty is not None:
            quantity = order_line.product_uom_qty + (add_qty or 0)

        # Remove zero of negative lines
        if quantity <= 0:
            order_line.unlink()
        else:
            # update line
            values = self._website_product_id_change(self.id, product_id, qty=quantity)
            if self.pricelist_id.discount_policy == 'with_discount' and not self.env.context.get('fixed_price'):
                order = self.sudo().browse(self.id)
                product_context = dict(self.env.context)
                product_context.setdefault('lang', order.partner_id.lang)
                product_context.update({
                    'partner': order.partner_id.id,
                    'quantity': quantity,
                    'date': order.date_order,
                    'pricelist': order.pricelist_id.id,
                })
                # Change product template by rental service, including price_unit by pricelist items
                product = self.env['product.product'].with_context(product_context).browse(product_id)
                product_rental_id = product.rental_service_ids[0] if product.rental_service_ids else product
                pu = self.env['account.tax']._fix_tax_included_price_company(product_rental_id.price,
                                                                             product_rental_id.taxes_id,
                                                                             order_line[0].tax_id,
                                                                             self.company_id)
                values.update({
                    'product_id': product_rental_id.id,
                    'product_uom': product_rental_id.uom_id.id,
                    'price_unit': pu,
                    'start_date': product_context['start_date'],
                    'end_date': product_context['end_date'],
                    'number_of_days': product_context['number_of_days'],
                })

            order_line.write(values)

        return {'line_id': order_line.id, 'quantity': quantity}
