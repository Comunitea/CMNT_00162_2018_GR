# -*- coding: utf-8 -*-
# © 2019 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Custom website quote',
    'version': '10.0.1.0.0',
    'category': 'website',
    'author': 'Comunitea',
    'maintainer': 'Comunitea',
    'website': 'www.comunitea.com',
    'license': 'AGPL-3',
    'depends': [
        'website_quote',
        'website_sale_charge_payment_fee',
        'payment_acquirer_by_amount'
    ],
    'data': [
        'views/website_quote_templates.xml',
        'views/payment.xml'
    ],
    'installable': True,
}
