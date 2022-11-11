# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by 73lines
# See LICENSE file for full copyright and licensing details.

from odoo import http
import string
from odoo.http import request
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.website_sale.controllers.main import TableCompute
from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.website.controllers.main import Website
from odoo import fields


# ppg = 20  # Products Per Page
# PPR = 4  # Products Per Row

class TableCompute(object):

    def __init__(self):
        self.table = {}

    def _check_place(self, posx, posy, sizex, sizey, ppr):
        res = True
        for y in range(sizey):
            for x in range(sizex):
                if posx + x >= ppr:
                    res = False
                    break
                row = self.table.setdefault(posy + y, {})
                if row.setdefault(posx + x) is not None:
                    res = False
                    break
            for x in range(ppr):
                self.table[posy + y].setdefault(x, None)
        return res

    def process(self, products, ppg=20, ppr=4):
        # Compute products positions on the grid
        minpos = 0
        index = 0
        maxy = 0
        x = 0
        for p in products:
            x = min(max(p.website_size_x, 1), ppr)
            y = min(max(p.website_size_y, 1), ppr)
            if index >= ppg:
                x = y = 1

            pos = minpos
            while not self._check_place(pos % ppr, pos // ppr, x, y, ppr):
                pos += 1
            # if 21st products (index 20) and the last line is full (ppr products in it), break
            # (pos + 1.0) / ppr is the line where the product would be inserted
            # maxy is the number of existing lines
            # + 1.0 is because pos begins at 0, thus pos 20 is actually the 21st block
            # and to force python to not round the division operation
            if index >= ppg and ((pos + 1.0) // ppr) > maxy:
                break

            if x == 1 and y == 1:   # simple heuristic for CPU optimization
                minpos = pos // ppr

            for y2 in range(y):
                for x2 in range(x):
                    self.table[(pos // ppr) + y2][(pos % ppr) + x2] = False
            self.table[pos // ppr][pos % ppr] = {
                'product': p, 'x': x, 'y': y,
                'ribbon': p.website_ribbon_id,
            }
            if index <= ppg:
                maxy = max(maxy, y + (pos // ppr))
            index += 1

        # Format table according to HTML needs
        rows = sorted(self.table.items())
        rows = [r[1] for r in rows]
        for col in range(len(rows)):
            cols = sorted(rows[col].items())
            x += len(cols)
            rows[col] = [r[1] for r in cols if r[1]]

        return rows

# class WebsiteProductLimit(http.Controller):
#
#     @http.route(['/shop/product_limit'], type='json', auth="public")
#     def change_limit(self, value):
#         global ppg
#         ppg = int(value)
#         return True


class WebsiteSaleExt(WebsiteSale):

    def _get_search_domain_ext(self, search, category, attrib_values,
                               tag_values, brand_values, price_min, price_max, rating):
        domain = request.website.sale_product_domain()

        if search:
            for srch in search.split(" "):
                domain += [
                    '|', '|', '|', ('name', 'ilike', srch),
                    ('description', 'ilike', srch),
                    ('description_sale', 'ilike', srch),
                    ('product_variant_ids.default_code', 'ilike', srch)]

        if category:
            domain += [('public_categ_ids', 'child_of', int(category))]

        if attrib_values:
            attrib = None
            ids = []
            for value in attrib_values:
                if not attrib:
                    attrib = value[0]
                    ids.append(value[1])
                elif value[0] == attrib:
                    ids.append(value[1])
                else:
                    domain += [('attribute_line_ids.value_ids', 'in', ids)]
                    attrib = value[0]
                    ids = [value[1]]
            if attrib:
                domain += [('attribute_line_ids.value_ids', 'in', ids)]

        if tag_values:
            domain += [('tag_ids', 'in', tag_values)]

        if brand_values:
            domain += [('brand_id', 'in', brand_values)]

        if price_min:
            domain += [('list_price', '>=', price_min)]

        if price_max:
            domain += [('list_price', '<=', price_max)]

        if rating is not None:
            domain += [('id', 'in', rating)]

        return domain

    @http.route()
    def shop(self, page=0, category=None, search='', min_price=0.0, max_price=0.0, ppg=False, **post):

        if ppg:
            try:
                ppg = int(ppg)
                post['ppg'] = ppg
            except ValueError:
                ppg = False
        if not ppg:
            ppg = request.env['website'].get_current_website().shop_ppg or 20

        ppr = request.env['website'].get_current_website().shop_ppr or 4
        try:
            min_price = float(min_price)
        except ValueError:
            min_price = False
        try:
            max_price = float(max_price)
        except ValueError:
            max_price = False
        # For Attributes
        attrib_list = request.httprequest.args.getlist('attrib')
        attrib_values = [list(map(int, v.split("-"))) for v in attrib_list if v]
        attributes_ids = set([v[0] for v in attrib_values])
        attrib_set = set([v[1] for v in attrib_values])
        ProductAttributeCount = request.env['product.template']

        # For Tags
        tag_list = request.httprequest.args.getlist('tags')
        tag_values = [list(map(str, v.split("-"))) for v in tag_list if v]
        tag_set = set([int(v[1]) for v in tag_values])
        ProductTagCount = request.env['product.template']

        rating_dict = {}
        for i in range(1,5):
            rating_dict[i] = 0
        # For Brands
        brand_list = request.httprequest.args.getlist('brands')
        brand_values = [list(map(str, v.split("-"))) for v in brand_list if v]
        brand_set = set([int(v[1]) for v in brand_values])
        rating_list = request.httprequest.args.getlist('ratings')
        Product = request.env['product.template'].sudo().search([])
        rating_ids = None
        if post.get('ratings'):
            rating_ids = []
            if rating_list:
                for j in rating_list:
                    for i in Product:
                        if i.rating_avg >= float(j):
                            rating_ids.append(i.id)

        for j in range(1,5):
            for i in Product:
                if i.rating_avg >= float(j):
                    rating_dict[int(j)] += 1
        #Category Count
        ProductCountTemplate = request.env['product.template']
        Product = ProductCountTemplate.with_context(bin_size=True)
        domain = self._get_search_domain(search, None, attrib_values)
        search_product = Product.search(domain)
        brand_count = Product._get_product_brand_count(website_ids=request.website.ids, product_ids=search_product.ids)
        tag_count = ProductTagCount._get_product_tag_count(website_ids=request.website.ids, product_ids=search_product.ids)
        attribute_count = ProductAttributeCount._get_product_attribute_count(website_ids=request.website.ids, product_ids=search_product.ids)
        get_count = ProductCountTemplate._get_product_categories_count(website_ids=request.website.ids, product_ids=search_product.ids)


    # Price Filter Condition
        categ_products = None
        if category:
            categ_products = Product.search([
                ('website_published', '=', True),
                ('public_categ_ids', 'child_of', int(category))])
            if categ_products:
                products_price = [product.list_price for product in categ_products]
                products_price.sort()
                price_min_range = products_price and products_price[0]
                price_max_range = products_price and products_price[-1]

                if request.httprequest.args.getlist('price_min') \
                        and request.httprequest.args.getlist('price_min')[0] != '':
                    price_min = float(request.httprequest.args.getlist('price_min')[0])
                else:
                    price_min = 0.0

                if request.httprequest.args.getlist('price_max') \
                        and request.httprequest.args.getlist('price_max')[0] != '':
                    price_max = float(request.httprequest.args.getlist('price_max')[0])
                else:
                    price_max = 0.0
            else:
                price_max = price_min = price_min_range = price_max_range = 0.0
        else:
            price_max = price_min = price_min_range = price_max_range = 0.0

        domain = self._get_search_domain_ext(search, category, attrib_values,
                                             list(tag_set), list(brand_set),
                                             min_price, max_price, rating = rating_ids)
        rating = 0
        keep = QueryURL('/shop', category=category and int(category),
                        search=search, attrib=attrib_list,
                        order=post.get('order'), brands=brand_list,
                        tags=tag_list, price_min=price_min, rating=4,
                        price_max=price_max)

        url = "/shop"
        if category:
            category = request.env['product.public.category'].browse(
                int(category))
            url = "/shop/category/%s" % slug(category)
        if attrib_list:
            post['attrib'] = attrib_list
        if tag_list:
            post['tags'] = tag_list
        if brand_list:
            post['brands'] = brand_list
        if rating:
            post['rating'] = rating

        product_count = Product.search_count(domain)
        pager = request.website.pager(url=url, total=product_count,
                                      page=page, step=ppg, scope=7,
                                      url_args=post)
        products = Product.search(domain, limit=ppg, offset=pager['offset'],
                                  order=self._get_search_order(post))
        ProductAttribute = request.env['product.attribute']
        ProductBrand = request.env['product.brand']
        ProductTag = request.env['product.tags']
        if products:
            attributes = ProductAttribute.search(
                [('attribute_line_ids.product_tmpl_id', 'in', products.ids)])
            prod_brands = []
            prod_tags = []
            for product in products:
                if product.brand_id:
                    prod_brands.append(product.brand_id.id)
                if product.tag_ids:
                    for tag_id in product.tag_ids.ids:
                        prod_tags.append(tag_id)
            brands = ProductBrand.browse(list(set(prod_brands)))
            tags = ProductTag.browse(list(set(prod_tags)))

        else:
            attributes = ProductAttribute.browse(attributes_ids)
            brands = ProductBrand.browse(brand_set)
            tags = ProductTag.browse(tag_set)

        # limits = request.env['product.view.limit'].search([])

        res = super(WebsiteSaleExt, self).shop(page=page, category=category,
                                               search=search, ppg=ppg, min_price=min_price, max_price=max_price, **post)
        res.qcontext.update({
            'pager': pager, 'products': products, 'tags': tags,
            'brands': brands,
            'bins': TableCompute().process(products, ppg,ppr),
            'attributes': attributes, 'search_count': product_count,
            'attrib_values': attrib_values, 'tag_values': tag_values,
            'brand_values': brand_values, 'brand_set': brand_set,
            'attrib_set': attrib_set, 'tag_set': tag_set,
            # 'attrib_set': attrib_set, 'tag_set': tag_set, 'limits': limits,
            'ppg': ppg, 'price_min_range': price_min_range,
            'price_max_range': price_max_range, 'price_min': price_min,
            'price_max': price_max, 'keep': keep,
            'categ_products': categ_products,
            'brand_count': brand_count,
            'tag_count': tag_count,
            'attribute_count': attribute_count,
            'get_count' : get_count,
            'rating_list' : rating_list,
            'rating_dict': rating_dict,
        })
        return res

    @http.route()
    def product(self, product, category='', search='', **kwargs):
        ProductCategory = request.env['product.public.category']
        if category:
            category = ProductCategory.browse(int(category)).exists()

        # For Attributes
        attrib_list = request.httprequest.args.getlist('attrib')
        attrib_values = [list(map(int, v.split("-"))) for v in attrib_list if v]
        attrib_set = set([v[1] for v in attrib_values])

        # For Tags
        tag_list = request.httprequest.args.getlist('tags')
        tag_values = [list(map(str, v.split("-"))) for v in tag_list if v]
        tag_set = set([int(v[1]) for v in tag_values])

        # For Brands
        brand_list = request.httprequest.args.getlist('brands')
        brand_values = [list(map(str, v.split("-"))) for v in brand_list if v]
        brand_set = set([int(v[1]) for v in brand_values])


        if request.httprequest.args.getlist('price_min') \
                and request.httprequest.args.getlist('price_min')[0] != '':
            price_min = float(request.httprequest.args.getlist('price_min')[0])
        else:
            price_min = False

        if request.httprequest.args.getlist('price_max') \
                and request.httprequest.args.getlist('price_max')[0] != '':
            price_max = float(request.httprequest.args.getlist('price_max')[0])
        else:
            price_max = False

        keep = QueryURL('/shop', category=category and category.id,
                        search=search, attrib=attrib_list,
                        brands=brand_list, tags=tag_list, price_min=price_min,
                        price_max=price_max)

        res = super(WebsiteSaleExt, self).product(product=product,
                                                  category=category,
                                                  search=search, **kwargs)

        res.qcontext.update({
            'attrib_values': attrib_values,
            'attrib_set': attrib_set,
            'tag_values': tag_values,
            'tag_set': tag_set,
            'brand_values': brand_values,
            'brand_set': brand_set,
            'keep': keep,
            'price_min': price_min,
            'price_max': price_max,


        })
        return res

    @http.route('/shop/cart/sidebar', type='json', website=True, auth='public')
    def get_shop_cart_sidebar_content(self):
        val = {}
        order = request.website.sale_get_order()
        val.update({
            'cart_lines': request.env['ir.ui.view']._render_template("website_product_misc_options_ul_73lines.ultimate_sidebar_cart", {
                'website_sale_order': order,
                'date': fields.Date.today(),
                'suggested_products': order._cart_accessories()
            }),
            'short_cart_summary': request.env['ir.ui.view']._render_template("website_product_misc_options_ul_73lines.ultimate_sidebar_cart_short_summary", {
                'website_sale_order': order,
            })
        })
        return val

    @http.route()
    def cart_update_json(self, product_id, line_id=None, add_qty=None, set_qty=None, display=True, **kw):
        res = super(WebsiteSaleExt, self).cart_update_json(product_id=product_id, line_id=line_id, add_qty=add_qty,
                                                           set_qty=set_qty, display=display, **kw)
        order = request.website.sale_get_order()
        res['website_sale.cart_lines'] = request.env['ir.ui.view']._render_template(
            "website_product_misc_options_ul_73lines.ultimate_sidebar_cart", {
                'website_sale_order': order,
                'date': fields.Date.today(),
                'suggested_products': order._cart_accessories()
            })
        res['website_sale.short_cart_summary_sidebar'] = request.env['ir.ui.view']._render_template(
            "website_product_misc_options_ul_73lines.ultimate_sidebar_cart_short_summary", {
                'website_sale_order': order,
            })
        return res

    @http.route('/shop/clear/cart', website=True, type='json', auth='public')
    def shop_clear_cart(self, **post):
        order = request.website.sale_get_order()
        order.order_line = False
        return True

# class Website(Website):
#
#     @http.route()
#     def toggle_switchable_view(self, view_key):
#         super(Website, self).toggle_switchable_view(view_key)
#         if view_key == 'website_product_misc_options_ul_73lines.categories_count':
#             request.website.viewref('website_product_misc_options_ul_73lines.categories_count_recursive_c').toggle_active()

    @http.route('/brand-list', type='http', auth='public', website=True)
    def brand_listing_page(self, **post):
        data = {}
        for alphabet in list(string.ascii_lowercase):
            data[alphabet] = request.env['product.brand'].sudo().search([('name', '=ilike', alphabet + '%')])
        brands = request.env['product.brand'].sudo().search([], order='name ASC')
        ProductCountTemplate = request.env['product.template']
        Product = ProductCountTemplate.with_context(bin_size=True)
        domain = self._get_search_domain(False, None, False)
        search_product = Product.search(domain)
        brand_count = Product._get_product_brand_count(website_ids=request.website.ids, product_ids=search_product.ids)
        return request.render('website_product_misc_options_ul_73lines.brand-listing', {
            'brands': brands,
            'brand_count': brand_count,
            'data': data,
        })
