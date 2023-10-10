# -*- coding: utf-8 -*-
from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    actual_customer_id = fields.Many2one('res.partner')
    vip_discount_id = fields.Many2one('vip.discount')
