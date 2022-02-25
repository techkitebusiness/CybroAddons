# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2021-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: odoo@cybrosys.com
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

from odoo import fields, models, api, _


class SaleOrderConfirm(models.Model):
    _inherit = 'sale.order'

    def action_multi_confirm(self):

        for order in self.env['sale.order'].browse(self.env.context.get('active_ids')).filtered(
                lambda o: o.state in ['draft', 'sent']):
            order.action_confirm()

    def action_multi_cancel(self):

        for order in self.env['sale.order'].browse(self.env.context.get('active_ids')):
            order.action_cancel()
