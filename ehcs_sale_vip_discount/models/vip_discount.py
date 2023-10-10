# -*- coding: utf-8 -*-
from uuid import uuid4

from odoo import api, fields, models


class VIPDiscount(models.Model):
    _name = 'vip.discount'
    _description = 'VIP Discount'
    _rec_name = 'code'

    code = fields.Char(
        string='Code',
        default=lambda self: self._generate_code(),
        copy=False, required=True)
    customer_id = fields.Many2one(
        'res.partner', string='Customer',
        required=True)
    expire_date = fields.Date(
        string='Valid Until', 
        required=True)
    pricelist_id = fields.Many2one(
        'product.pricelist', string='Pricelist',
        required=True)
    valid_code = fields.Char(
        string='Code & Valid Until',
        copy=False, compute='_compute_valid_code')
    state = fields.Selection([
        ('active', 'Active'),
        ('used', 'Used'),
        ('expired', 'Expired'),
        ('inactive', 'In-Active')
    ], readonly=True, string='State', default='active')
    
    @api.model
    def _generate_code(self):
        """ VIP Discount code """
        return str(uuid4())[9:-13]

    @api.depends('code','expire_date')
    def _compute_valid_code(self):
        for vip in self:
            vip.valid_code = 'Code: '+ str(vip.code) + '\nValid Until: '+ str(vip.expire_date)

    def action_inactive(self):
        """ In-active record using button """
        self.write({'state': 'inactive'})

    def expired_vip_discount_cron(self):
        """Expired records via scheduler"""
        vip_discounts = self.search([
            ('state', '=', 'active'),
            ('expire_date', '<', fields.Date.today())
        ])
        vip_discounts.write({'state': 'expired'})
        return True
