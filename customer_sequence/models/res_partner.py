# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2020-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Midilaj (<https://www.cybrosys.com>)
#
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    unique_id = fields.Char(string='Unique Id', help="The Unique Sequence no", readonly=True, default='/')

    @api.model
    def create(self, values):
        res = super(ResPartner, self).create(values)
        company_seq = self.env.company
        if res.customer_rank > 0 and res.unique_id == '/':
            if company_seq.next_code:
                res.unique_id = company_seq.next_code
                res.name = '[' + str(company_seq.next_code) + ']' + str(res.name)
                company_seq.write({'next_code': company_seq.next_code + 1})
            else:
                res.unique_id = company_seq.customer_code
                res.name = '[' + str(company_seq.customer_code) + ']' + str(res.name)
                company_seq.write({'next_code': company_seq.customer_code + 1})
        return res
