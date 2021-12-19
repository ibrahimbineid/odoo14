# -*- coding: utf-8 -*-


from odoo import models, fields, api, _


class ProductInherit(models.Model):
    _inherit = 'product.template'

    ip_address = fields.Char(string='IP Address')
    item_type = fields.Char('Item Type')
    item_brands = fields.Many2many('product.brand')
    item_models = fields.Many2many('product.model')
    
    @api.onchange('item_brands')
    def onchange_item_brands(self):
        if self.item_brands:
            self.item_models = False
            for recs in self.item_brands:
                site_list = []
                sites = self.env['product.brand'].search([('name', '=', recs.name)])
                if sites:
                    for rec in sites:
                        for recd in rec.model:
                            site_list.append(recd.id)
                if self.item_models:
                    for rec_model in self.item_models:
                        site_list.append(rec_model.id)
                self.item_models = site_list
        else:
            self.item_models = False


class ProductModel(models.Model):
    _name = 'product.model'
    name = fields.Char(String='Item Model')
    
    
class ProductModel(models.Model):
    _name = 'product.brand'
    name = fields.Char(String='Item Brands')
    model = fields.Many2many('product.model', string='Item Models')
