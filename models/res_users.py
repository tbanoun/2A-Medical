# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ResUsers(models.Model):
    _name = "res.users"
    _inherit = "res.users"

    # product_category = fields.Many2many(
    #     "product.category",
    #     string="Product Category",
    # )

    # customer_category = fields.Many2many(
    #     "customer.category",
    #     string="Customer Category",
    # )

    # user_zone_ids = fields.Many2many("customer_zone", string="Zone IDS")
    # # enregistre les zones selectionner pour ce clients
    # zone_list = fields.Char(
    #     compute="_compute_user_commune_domain", readonly=True, store=True, default="[]"
    # )

    # user_commune = fields.Many2many("customer_commune", string="Commune")
    # commune_domain = fields.Char(
    #     compute="_compute_user_commune_domain", readonly=True, store=True
    # )
    # res_partner_domain = fields.Char(
    #     compute="_compute_user_commune_domain", readonly=True, store=True
    # )

    # res_partner_current_user = fields.Char("_compute_res_partner_current", readonly=True, store=True)
    # res_partner = fields.Many2many("res.partner")

    # @api.onchange("user_zone_ids")
    # def empty_data(self):
    #     for rec in self:
    #         rec.user_commune = False
    #         rec.res_partner = False

    # @api.depends("user_zone_ids")
    # def _compute_user_commune_domain(self):
    #     for rec in self:
    #         if rec.user_zone_ids:
    #             zone_names = rec.user_zone_ids.mapped("name")
    #             rec.commune_domain = '[("zone", "in", %s)]' % repr(zone_names)
    #             rec.res_partner_domain = '[("zone", "in", %s)]' % repr(zone_names)
    #             rec.zone_list = repr(zone_names)
    #         else:
    #             rec.commune_domain = "[]"
    #             rec.res_partner_domain = "[]"
    #             rec.zone_list = "[]"

    # @api.depends("user_zone")
    # def find_commune(self):
    #     for rec in self:
    #         if rec.user_zone:
    #             print("user zone ids*********************", rec.user_zone)
    #             rec.user_commune = False
    #             if any(zone for zone in rec.user_zone):
    #                 # Logique pour trouver les communes basées sur les zones
    #                 print("rec user zone name---------------------", [rec.user_zone])
    #                 commune_ids = self.env["_commune"].search(
    #                     [("zone", "in", rec.user_zone)]
    #                 )
    #                 print("coucouccccccccccccccccccccc", commune_ids)
    #                 rec.user_commune = commune_ids
    #                 rec.partner_cnt = len(commune_ids)
    #         else:
    #             # cette ligne evitera le bug
    #             rec.user_commune = [()]
    #             rec.partner_cnt = 0
    # # donnez aux clients le ID du user selectionner
    # @api.depends("user_zone_ids")
    # def _compute_res_partner_current(self):
        
    #     for rec in self:
    #         if rec.id:
    #             rec.res_partner_current_user = rec.id
            

    # # Logique pour trouver les communes basées sur les zones
    # # Exemple simplifié : trouver les communes qui appartiennent à ces zones
    # # commune_ids = self.env["_commune"].search([("zone", "in", ["OUEST"])])
    # # rec.user_commune = [(commune_ids)]
    # # rec.partner_cnt = len(commune_ids)
    # # else:
    # # rec.user_commune = [()]
    # # rec.partner_cnt = 0
    # #     print("xxxxxxxxxxxxxxxxxxxxxxxxxx", self.user_zone)
    # #     domain_zone_ids = self.user_zone.mapped("name")
    # #     print("ssssssssssssssssssssssssssssssssssss,", domain_zone_ids)
    # #     return {"domain": {"user_commune": [("zone", "in", domain_zone_ids)]}}
    # # else:
    # #     return {"domain": {"user_commune": []}}

    # # @api.depends("user_zone")
    # # def default_get(self, fields_list):
    # #     res = super("_commune", self).default_get(fields_list)
    # #     print("acesssssssssssssssssssssssssssssssssss")
    # #     res.update(
    # #         {
    # #             "user_commune": self.env["_commune"]
    # #             .search([("zone", "in", ["CENTRE"])])
    # #             .id,
    # #         }
    # #     )
    # #     return res

    # # @api.depends("user_zone")
    # # def find_commune(self):
    # #     print("xxxxxxxxxxxxxxxxxxxxxxxxxx", self.user_zone)
    # # if self.user_zone:
    # #     print("xxxxxxxxxxxxxxxxxxxxxxxxxx", self.user_zone)
    # #     domain_zone_ids = self.user_zone.mapped("name")
    # #     print("ssssssssssssssssssssssssssssssssssss,", domain_zone_ids)
    # #     return {"domain": {"user_commune": [("zone", "in", ["OUEST"])]}}
    # # else:
    # #     return {"domain": {"user_commune": []}}

    # # ('wilaya_id','=',user_wilaya),

    # # @api.depends("user_zone_ids", "user_customer_category")
    # # def partner_count(self):
    # #     for rec in self:
    # #         domain = []
    # #         if rec.user_wilaya.ids:
    # #             domain.append(("wilaya_id", "in", rec.user_wilaya.ids))
    # #         if rec.user_commune.ids:
    # #             domain.append(("commune_id", "in", rec.user_commune.ids))
    # #         if rec.user_customer_category.ids:
    # #             domain.append(("code_category", "in", rec.user_customer_category.ids))

    # #         print(
    # #             "lennnnnnnnnnnnnnnnnnnnnnn",
    # #             self.env["res.partner"].search_count(domain),
    # #         )
    # #         rec.partner_cnt = self.env["res.partner"].search_count(domain)
    # #         rec.user_domain = domain
    # #         if len(domain) == 0:
    # #             rec.user_domain = []
    # #         print("domainnnnnnnnnnnn", domain)

    # # @api.onchange("user_wilaya")
    # # def empty_commune(self):
    # #     for record in self:
    # #         record.user_commune = False
