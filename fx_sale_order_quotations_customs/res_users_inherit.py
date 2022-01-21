# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import models, fields, api


class ResUsersInherit(models.Model):
    _inherit = 'res.users'

    sh_pricelist_ids = fields.Many2many(
        'product.pricelist', 'res_users_product_pricelist_rel', string='Price List')


class PricelistInherit(models.Model):
    _inherit = 'product.pricelist'

    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        cr = self.env.cr
        team_ids = False
        team_pricelist_ids = []
        user_pricelist_ids = []
        generic_pricelist_ids = []
        finally_pricelist_ids = []
        cr.execute("""
                select crm_team_id from crm_team_member where user_id=%s group by crm_team_id;
            """, (self.env.user.id,))
        cr_res = cr.fetchall()
        if cr_res and cr_res[0] and cr_res[0][0]:
            team_ids = [x[0] for x in cr_res]
        print ("###### team_ids >>>>>>> ", team_ids)
        ### Tarifas de Equipos de Venta #####
        if team_ids:
            cr_res = False
            if len(team_ids) == 1:
                cr.execute("""
                    select id from product_pricelist where team_id=%s;
                """, (self.env.user.id,))
                cr_res = cr.fetchall()
            else:
                cr.execute("""
                    select id from product_pricelist where team_id in %s;
                """, (tuple(team_ids),))
                cr_res = cr.fetchall()
            if cr_res and cr_res[0] and cr_res[0][0]:
                team_pricelist_ids = [x[0] for x in cr_res]
        print ("###### team_pricelist_ids >>>>>>> ", team_pricelist_ids)
        ##### Tarifas de Usuarios ######
        cr.execute("""
            select id from product_pricelist where user_id=%s;
        """, (self.env.user.id,))
        cr_res = cr.fetchall()
        if cr_res and cr_res[0] and cr_res[0][0]:
            user_pricelist_ids = [x[0] for x in cr_res]
        ##### Tarifas de Usuarios ######
        print ("###### user_pricelist_ids >>>>>>> ", user_pricelist_ids)

        ##### Tarifas Generales ######
        # generic_pricelist_ids
        cr.execute("""
            select id from product_pricelist where user_id is null and team_id is null;
        """, (self.env.user.id,))
        cr_res = cr.fetchall()
        if cr_res and cr_res[0] and cr_res[0][0]:
            generic_pricelist_ids = [x[0] for x in cr_res]
        print ("###### generic_pricelist_ids >>>>>>> ", generic_pricelist_ids)

        ### Sumando todas las Tarifas ###
        finally_pricelist_ids = team_pricelist_ids + user_pricelist_ids + generic_pricelist_ids
        print ("###### finally_pricelist_ids >>>>>>> ", finally_pricelist_ids)
        if finally_pricelist_ids:
            args.append(('id', 'in', finally_pricelist_ids))
        res = super(PricelistInherit, self)._search(args, offset=offset, limit=limit,
                                                    order=order, count=count, access_rights_uid=access_rights_uid)

        return res


    