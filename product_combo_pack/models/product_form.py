# -*- coding: utf-8 -*-
###################################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2020-TODAY Cybrosys Technologies (<https://www.cybrosys.com>).
#    Author: Afras Habis (odoo@cybrosys.com)
#
#    This program is free software: you can modify
#    it under the terms of the GNU Affero General Public License (AGPL) as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
###################################################################################

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ProductPack(models.Model):
    _inherit = 'product.template'

    def default_pack_location(self):
        company_user = self.env.company
        warehouse = self.env['stock.warehouse'].search([('company_id', '=', company_user.id)], limit = 1)
        if warehouse:
            return warehouse.lot_stock_id.id

    is_pack = fields.Boolean('Is a Pack')
    pack_price = fields.Integer(string = "Pack Price", compute = 'set_pack_price', store = True)
    pack_products_ids = fields.One2many('pack.products', 'product_tmpl_id', string = 'Pack Products')
    pack_quantity = fields.Integer('Pack Quantity')
    pack_location_id = fields.Many2one('stock.location',
                                       domain = [('usage', 'in', ['internal', 'transit'])],
                                       default = default_pack_location)

    @api.depends('pack_products_ids', 'pack_products_ids.price')
    def set_pack_price(self):
        price = 0
        for record in self:
            for line in record.pack_products_ids:
                price = price + line.price
            record.pack_price = price

    @api.model
    def create(self, values):
        if values.get('is_pack', False):
            if not values.get('pack_products_ids', []):
                raise UserError(_(
                    'You need to add atleast one product in the Pack...!'))
            if values.get('type', False) == 'service':
                raise UserError(_('You cannot define a pack product as a service..!'))
        return super(ProductPack, self).create(values)

    def write(self, values):
        super(ProductPack, self).write(values)
        if self.is_pack:
            if not self.pack_products_ids:
                raise UserError(_(
                    'You need to add atleast one product in the Pack...!'))
            if self.type == 'service':
                raise UserError(_('You cannot define a pack product as a service..!'))

    def update_price_product(self):
        self.lst_price = self.pack_price

    def get_quantity(self):
        total_quantity = 1
        flag = 1
        while flag:
            for line in self.pack_products_ids:
                if line.qty_available >= line.quantity * total_quantity:
                    continue
                else:
                    if line.product_id.type != 'product':
                        continue
                    flag = 0
                    break
            if flag:
                total_quantity = total_quantity + 1
        self.pack_quantity = total_quantity - 1

    def update_quantity(self):
        company_user = self.env.company
        product_id = len(self.product_variant_ids) == 1 and self.product_variant_id.id
        location_id = self.pack_location_id.id
        if not location_id:
            warehouse = self.env['stock.warehouse'].search([('company_id', '=', company_user.id)], limit = 1)
            location_id = warehouse.lot_stock_id.id
            if not location_id:
                raise UserError(_(
                    'You need to select the location to update the pack quantity...!'))
        self.env['stock.quant'].with_context(inventory_mode = True).sudo().create({
            'product_id': product_id,
            'location_id': location_id,
            'inventory_quantity': self.pack_quantity,
        })

    @api.onchange('pack_location_id')
    def change_quantity_based_on_location(self):
        for line in self.pack_products_ids:
            stock_quant = self.env['stock.quant'].search(
                [('product_id', '=', line.product_id.id), ('location_id', '=', self.pack_location_id.id)])
            if stock_quant:
                line.total_available_quantity = stock_quant.quantity

            else:
                line.total_available_quantity = stock_quant.quantity