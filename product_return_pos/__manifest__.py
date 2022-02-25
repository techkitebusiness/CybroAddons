# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2021-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Anusha P P (odoo@cybrosys.com)
#
#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
{
    'name': 'Product Return In POS',
    'version': '15.0.1.0.0',
    'category': 'Point of Sale',
    'summary': 'POS Order Return',
    'author': 'Cybrosys Techno Solutions',
    'company': 'Cybrosys Techno Solutions',
    'maintainer': 'Cybrosys Techno Solutions',
    'images': ['static/description/banner.png'],
    'website': 'https://www.cybrosys.com',
    'depends': ['point_of_sale'],
    'data': [
             'views/return.xml',
            ],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
    'assets': {
        'point_of_sale.assets': [
            'product_return_pos/static/src/css/pos_return.css',
            'product_return_pos/static/src/js/pos_return.js',
            'product_return_pos/static/src/js/return.js',
            'product_return_pos/static/src/js/models.js',
            'product_return_pos/static/src/js/order_list_screen.js'
        ],
        'web.assets_qweb': [
            'product_return_pos/static/src/xml/pos_return.xml',
        ],
    },
}


