# -*- coding: utf-8 -*-

from odoo import models, fields


class Website(models.Model):
    _inherit = 'website'

    social_instagram = fields.Char('Instagram Account')


class WebsiteConfigSettings(models.TransientModel):
    _inherit = 'website.config.settings'

    website_id = fields.Many2one('website', string="website", default=1, required=True)
    social_instagram = fields.Char(related='website_id.social_instagram')
    domain = fields.Char(related='website_id.domain')
