# -*- coding: utf-8 -*-
# © 2019 Comunitea
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
        'payment_redsys',
        'sale_rental',
        'theme_bootswatch',
        'web_sheet_full_width',
        'website_portal',
        'website_cookie_notice',
        'website_crm',
        'website_crm_privacy_policy',
        'website_crm_recaptcha',
        'website_form_recaptcha',
        'website_legal_page',
        'website_signup_legal_page_required',
        'website_sale',
        'website_sale_filter_countries',
        'website_sale_require_login',
        'website_sale_one_step_checkout',
        'website_sale_one_step_checkout_delivery',
    ],
    'data': [
        'data/menu_data.xml',
        'templates/cart.xml',
        'templates/checkout.xml',
        'templates/contactus.xml',
        'templates/footer.xml',
        'templates/header.xml',
        'templates/product.xml',
        'templates/shop.xml',
        'templates/order.xml',
        'templates/views.xml',
        'templates/res_config.xml',
    ],
    'images': [
        'static/description/icon.png'
    ],
    'website': 'http://www.comunitea.com',
    'installable': True,
}
