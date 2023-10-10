# -*- coding: utf-8 -*-

from datetime import datetime

from odoo import fields, http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteVIPDiscount(WebsiteSale):

    @http.route(
        ['/shop/pricelist'], type='http', auth="public", website=True, sitemap=False
    )
    def pricelist(self, promo, **post):
        redirect = post.get('r', '/shop/cart')
        today = fields.Date.today()
        domain = [('code', '=', promo), ('expire_date', '>=', today), ('state', '=', 'active')]
        vip_discount = request.env['vip.discount'].sudo().search(domain, limit=1)
        if vip_discount:
            pricelist_sudo = vip_discount.pricelist_id
            request.session['website_sale_current_pl'] = pricelist_sudo.id
            if not (pricelist_sudo and request.website.is_pricelist_available(pricelist_sudo.id)):
                return request.redirect("%s?code_not_available=1" % redirect)

            order_sudo = request.website.sale_get_order(force_create=True)
            # Update Actual customer and VIP Discount on sale order
            order_sudo.update({
                'actual_customer_id': vip_discount.customer_id.id,
                'vip_discount_id': vip_discount.id,
            })
            # Update VIP Discount state
            vip_discount.update({'state': 'used'})
            order_sudo._cart_update_pricelist(pricelist_id=pricelist_sudo.id)
        else:
            return super(WebsiteVIPDiscount, self).pricelist(promo, **post)
        return request.redirect(redirect)
