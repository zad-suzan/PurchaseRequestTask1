# -*- coding: utf-8 -*-
from odoo import api, fields, models


class PurchaseRequestLine(models.Model):
    _name = "purchase.request.line"
    _description = "Purchase Request Line"
    _inherit = []

    product_id = fields.Many2one("product.product", string="Product", required=True)
    Description = fields.Char(string='Description', related="product_id.name")
    Quantity = fields.Float(string="Quantity", default=1)
    Cost = fields.Float(string="Cost Price", related = 'product_id.standard_price', readonly=True)
    Total = fields.Float(string='Total', compute='_compute_total', readonly=True)
    pur_req_id = fields.Many2one('purchase.request', string='Purchase Request')

    @api.depends('Quantity','Cost')
    def _compute_total(self):
        for rec in self:
            rec.Total = rec.Quantity * rec.Cost