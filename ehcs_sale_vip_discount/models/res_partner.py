# -*- coding: utf-8 -*-
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def _compute_vip_orders_count(self):
        sale_obj = self.env['sale.order']
        for partner in self:
            partner.vip_orders_count = sale_obj.search_count(
                [('actual_customer_id', '=', self.id)]
            )
        return True 

    vip_orders_count = fields.Integer(
        'VIP Orders', compute='_compute_vip_orders_count'
    )

    def action_vip_discount(self):
        """ Open a VIP Discount form """
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id(
            "ehcs_sale_vip_discount.action_vip_discount"
        )
        action['context'] = {'default_customer_id': self.id}
        action['views'] = [
            (self.env.ref('ehcs_sale_vip_discount.vip_discount_view_form').id,
                'form')
        ]
        return action

    def open_vip_discount_orders(self):
        """ Get a VIP Discount orders """
        orders = self.env['sale.order'].search([
            ('actual_customer_id', '=', self.id),
            ('actual_customer_id', '!=', False)
        ]) 
        action = self.env["ir.actions.actions"]._for_xml_id(
            "sale.action_quotations_with_onboarding"
        )
        action.update({
            'context': {'default_customer_id': self.id},
            'views': False,
            'view_id': False,
        })
        if len(orders) == 1:
            action.update({
                'view_mode': 'form',
                'res_id': orders.id,
            })
        else:
            action['domain'] = [('id', 'in', orders.ids)]
        return action
