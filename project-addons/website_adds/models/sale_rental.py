# -*- coding: utf-8 -*-

from odoo import fields, models


class SaleRental(models.Model):
    _inherit = 'sale.rental'

    end_date = fields.Date(store=True)
