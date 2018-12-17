# -*- coding: utf-8 -*-
# © 2018 Comunitea
# Ruben Seijas <ruben@comunitea.com> - Pavel Smirnov <pavel@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    'name': 'Website adds',
    'version': '1.0',
    'summary': 'Website additional and customization theme',
    'author': 'Comunitea',
    'license': 'AGPL-3',
    'category': 'Custom',
    'depends': [
        'crm',
        'payment_redsys',
        'sale',
        'sale_rental',
        'stock',
        'theme_bootswatch',
        'web_sheet_full_width',
        'website',
        'website_cookie_notice',
        'website_crm',
        'website_crm_privacy_policy',
        'website_crm_recaptcha',
        'website_form_recaptcha',
        'website_legal_page',
        'website_sale',
        'website_sale_one_step_checkout',
        'website_sale_one_step_checkout_delivery',
        'website_sale_require_login',
        'website_signup_legal_page_required'
    ],
    'data': [
        'templates/cart.xml',
        'templates/checkout.xml',
        'templates/contactus.xml',
        'templates/footer.xml',
        'templates/header.xml',
        'templates/product.xml',
        'templates/shop.xml',
        'templates/views.xml'
    ],
    'images': [
        'static/description/icon.png'
    ],
    'website': 'http://www.comunitea.com',
    'installable': True,
}
