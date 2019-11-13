# -*- coding: utf-8 -*-

from odoo import fields, models


class PricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    website_name = fields.Char('Website Selector Name', required=True, help="Name for website selector")
    selectable = fields.Boolean('Website Selectable', default=False,
                                help="If checked, it will be selectable into the website selector.")
