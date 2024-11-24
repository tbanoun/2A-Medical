# -*- coding: utf-8 -*-
from requests.compat import basestring

from odoo import models, fields, api, _
from psycopg2 import errors
from odoo.exceptions import UserError
from odoo.exceptions import AccessError
from datetime import datetime


class ResPartner(models.Model):
    _name = "res.partner"
    _inherit = "res.partner"

    ref = fields.Char(string="Code Tiers", default="New", readonly=True)
    sponsored_by = fields.Many2many('res.partner', string="Parrainer par", compute="getAllSponredPartner")
    parrinage_id = fields.Many2one('res.partner', string='Related Company', index=True)
    sponsorship = fields.Many2many('res.partner', 'res_partner_sponsorship_rel', 'parrinage_id',  string='Parrainage')
    partner = fields.Many2one('res.partner', 'Contact')
    mobile = fields.Char(string="Mobile")
    gamme_id = fields.Many2one('product.gamme', string="Gamme de Produits")

    def getAllSponredPartner(self):
        for rec in self:
            partner_ids = self.env['res.partner'].sudo().search([
                ('sponsorship', 'in', [rec.id])
            ])
            if partner_ids:
                rec.sponsored_by = partner_ids.ids
            else:
                rec.sponsored_by = []

    @api.model
    def update_presence_status(self, status):
        try:
            self.env["bus.presence"].write({"status": status})
        except errors.SerializationFailure:
            # Réessayer l'opération
            self.update_presence_status(status)

    # incrementer ref
    def create(self, vals_list):
        print("\n\n",vals_list,"\n\n")
        # Si un dictionnaire unique est passé, on le transforme en liste
        if isinstance(vals_list, dict):
            vals_list = [vals_list]
        # Boucle sur chaque dictionnaire dans vals_list
        for vals in vals_list:
            # Vérifie que chaque élément est bien un dictionnaire
            if isinstance(vals, dict):
                # Assigner une valeur par défaut à "ref" si elle n'est pas présente
                if "ref" not in vals:
                    vals["ref"] = "New"

                # Définir la séquence si la référence est "New"
                if vals.get("ref") == "New":
                    vals["ref"] = self.env["ir.sequence"].next_by_code(
                        "res_partner_seq"
                    )

                # Convertir le nom en majuscules s'il est présent
                if "name" in vals and isinstance(vals['name'], basestring):
                    vals["name"] = vals["name"].upper()

        # Appeler la méthode create parent
        return super(ResPartner, self).create(vals_list)

    def write(self, vals):
        if "name" in vals:
            vals["name"] = vals["name"].upper()
        return super(ResPartner, self).write(vals)

    # # ['ouest','est']
    def unlink(self):
        user_id = self.env.user.id
        sale_team_id = self.env.user.team_id.id
        print("sale_team_id", sale_team_id)
        user = self.env["res.users"].browse(user_id)
        groups = user.groups_id
        group_names = user.groups_id.mapped("name")
        if "Master Data Manager" not in group_names:
            print("groups", group_names)
            raise UserError("La suppression des contacts est désactivée.")
        return super(ResPartner, self).unlink()

    # exemple record rules computed
    user_team_id = fields.Many2one(
        "crm.team", string="User's Sales Team", compute="_compute_user_team_id"
    )

    @api.depends("user_id")
    def _compute_user_team_id(self):
        for partner in self:
            partner.user_team_id = (
                self.env.user.sale_team_id.id if self.env.user.sale_team_id else False
            )

    # Exemple : vérifier si l'utilisateur actuel est dans un groupe spécifique
    # @api.onchange("country_id")
    # def get_user_groups(self):
    #     user_id = self.env.user.id
    #     user = self.env["res.users"].browse(user_id)
    #     groups = user.groups_id
    #     print("groups", groups.mapped("name"))
    #     return groups.mapped("name")

    def _get_potential(self):
        memeber_sales_team = self.env.user.team_id.crm_team_member_ids
        for rec in memeber_sales_team:
            print("reccccccccccc", rec)
        selection = []
        for emp in self.env["customer.potential"].search([], order="name asc"):
            selection += [("%s" % emp.id, "%s" % emp.description)]
        return selection

    def _get_adoption(self):
        selection = []
        for emp in self.env["customer.adoption"].search([], order="name asc"):
            selection += [("%s" % emp.id, "%s" % emp.description)]
        return selection

    def _get_solvency(self):
        selection = []
        for emp in self.env["customer.solvency"].search([]):
            selection += [("%s" % emp.id, "%s" % emp.description)]
        return selection

    def _get_sector(self):
        selection = []
        for emp in self.env["customer.sector"].search([]):
            selection += [("%s" % emp.id, "%s" % emp.description)]
        return selection

    def _get_leader(self):
        selection = []
        for emp in self.env["customer.leader"].search([]):
            selection += [("%s" % emp.id, "%s" % emp.description)]
        return selection

    # user qui controle ce client
    res_partner_user_id = fields.Many2many("res.users", "Responsable")
    # # wilaya et commune
    wilaya_id = fields.Many2one(
        "customer.wilaya", "Wilaya", domain="[('country_id','=',country_id)]"
    )

    commune_id = fields.Many2one(
        "customer.commune", "Commune", domain="[('wilaya_id','=',wilaya_id)]"
    )
    zone = fields.Char(related="commune_id.zone", string="Zone", store=True)

    locality_id = fields.Many2one(
        "customer.locality", "Localité", domain="[('wilaya_id','=',wilaya_id)]"
    )

    def _get_states(self):
        selection = []
        states = self.env["res.country.state"].search([("country_id", "=", "213")])
        selection = [(state.id, state.name) for state in states]
        return selection

    # set state_id to False if another country get selected
    @api.onchange("country_id")
    def empty_state(self):
        for record in self:
            record.wilaya_id = False
            record.commune_id = False
            record.locality_id = False

    @api.onchange("wilaya_id")
    def empty_commune(self):
        for record in self:
            record.commune_id = False
            record.locality_id = False

    @api.onchange("locality_id", "country_id", "wilaya_id")
    def get_zip(self):
        for record in self:
            if record.country_id and record.locality_id:  # type: ignore
                record.zip = record.locality_id.code  # type: ignore
            else:
                record.update({"zip": False})

    # traitement des categories is_company
    # @api.onchange("is_company")
    # def _onchange_is_company(self):
    #     if self.is_company is not None:
    #         categories = self._get_category()
    #         # Mettre à jour le champ de sélection ici
    #         self.code_category_selection = categories

    def _get_category(self):
        selection = []
        for emp in self.env["customer.category"].search(
            [("is_company", "=", self.is_company)]
        ):
            selection.append(("%s" % emp.id, "%s" % emp.description))
        return selection

    def _update_category_selection(self):
        categories = self._get_category()
        self.code_category = categories[0][0] if categories else False
        self.code_category_selection = categories

    @api.model
    def _get_default_category(self):
        selection = []
        for emp in self.env["customer.category"].search(
            [("is_company", "=", True)]  # type: ignore
        ):
            selection.append(("%s" % emp.id, "%s" % emp.description))
        return selection

    @api.depends("is_company")
    def _compute_category_selection(self):
        crmteam = self.crm_team_id
        print("crmteam", crmteam)
        for record in self:
            record.code_category_selection = record._get_category()

    def _get_default_category_selection(self):
        return self._get_category()

    @api.model
    def _get_category(self):
        selection = []
        for emp in self.env["customer.category"].search(
                [("is_company", "=", self.is_company)]
        ):
            selection += [("%s" % emp.id, "%s" % emp.description)]
        return selection

    @api.model
    def _get_type_freq(self):
        selection = []
        for emp in self.env["type.freq"].search([]):
            selection += [("%s" % emp.id, "%s" % emp.description)]
        return selection

    def _get_posfiscale(self):
        selection = []
        for emp in self.env["customer.posfiscale"].search([]):
            selection += [("%s" % emp.id, "%s" % emp.description)]
        return selection

    def _get_canal(self):
        selection = []
        canals = self.env["utm.medium"].search([])
        selection = [("%s" % canal.id, "%s" % canal.name) for canal in canals]
        return selection

    def _get_function(self):
        selection = []
        for emp in self.env["customer.function"].search([]):
            selection += [("%s" % emp.name, "%s" % emp.description)]
        return selection

    function_job = fields.Selection(_get_function, string="Job Function")
    code_potential = fields.Selection(_get_potential, string="Potentiel")
    code_adoption = fields.Selection(_get_adoption, string="Adoption")
    code_solvency = fields.Selection(_get_solvency, string="Solvabilité du client")
    code_leader = fields.Many2many("customer.leader", string="Leader d'opinion")
    code_category = fields.Many2one(
        "customer.category",
        string="Categorie",
        domain="[('is_company','=',is_company)]",
    )

    # code_category = fields.Char(string="Code Category")

    code_sector = fields.Selection(_get_sector, string="Secteur")

    code_persona = fields.Many2many("customer.persona", string="Persona")
    code_canal = fields.Many2many("utm.medium", string="Canal")
    code_interest = fields.Many2many("customer.interest", string="Interest")
    code_learning = fields.Many2many("customer.learning", string="Learning")
    code_typologie = fields.Many2many(
        "customer.typologie", string="Typologie de prescription"
    )
    code_product = fields.Many2many("product.template", string="Product")

    # frequence
    code_type_freq = fields.Selection(_get_type_freq, string="Frequency")
    freq_nbr = fields.Integer(string="Frequency number")
    freq_nbr_calc = fields.Integer(
        compute="_compute_frequency", string="Frequency number", store=True
    )

    @api.depends("freq_nbr", "code_type_freq")
    def _compute_frequency(self):
        for partner in self:
            existing_leads = self.env["crm.lead"].search(
                [("partner_id", "=", partner.id)]
            )
            if not existing_leads:
                for rec in partner:
                    # week
                    frequence = 0
                    if rec.code_type_freq == "1":
                        print("1111111", rec.code_type_freq)
                        print("1111111", rec.code_type_freq)
                        frequence = rec.freq_nbr * 12
                    # month
                    elif rec.code_type_freq == "2":
                        print("22", rec.code_type_freq)
                        print("22", rec.code_type_freq)
                        frequence = rec.freq_nbr * 3
                    # quarter
                    elif rec.code_type_freq == "3":
                        print("33", rec.code_type_freq)
                        print("33", rec.code_type_freq)
                        frequence = rec.freq_nbr * 1
                    rec.freq_nbr_calc = frequence
                    for i in range(frequence):
                        print("on est laaaaaaaaa", i)
                        new_leads = self.env["crm.lead"].create(
                            {
                                "name": "New Lead %s" % rec.name,
                                "partner_id": rec.id,  # Utilise l'ID du modèle de res.prtner
                                "type": "opportunity",
                            }
                        )

    # for rec in self:
    #     print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxx", rec.id)
    #     print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxx", existing_leads.ids)
    #     print("lennnnnnnnnnnnnnn", len(existing_leads))
    #     if existing_leads:
    #         for rec in existing_leads.ids:
    #             print("*****************", rec)

    # def create_frequency(self):
    #     # Vérifier que le produit existe
    #     # Obtenir la date actuelle
    #     aujourd_hui = datetime.now()

    #     # Calculer le trimestre
    #     trimestre = (aujourd_hui.month - 1) // 3 + 1

    #     print(f"Le trimestre actuel est T{trimestre}.")

    #     # calculer la frequence
    #     return True

    # journée de recption
    reception_day = fields.Many2many(
        "res.weekday",
        string="Reception day",
    )
    # # journée de recption
    reception_time = fields.Selection(
        [("morning", "Matin"), ("afternoon", "Apres midi"), ("night", "Soir")],
        string="Reception Time",
    )
    # # frequence de visite
    # line_id = fields.One2many("res.partner.frequency.line", "customer_id")

    def action_open_frequency(self):
        self._createRecordQuarter(self.id)
        action = self.env['ir.actions.act_window']._for_xml_id(
            'contacts_dnd.action_view_open_frequency2')
        action['context'] = {
            'default_partner_id': self.id,
            'search_default_group_by_lead_properties': True
        }
        action["domain"] = [('partner_id', '=', self.id)]
        return action

    def _createRecordQuarter(self, partner_id):
        year = datetime.now().year
        records = self.env['quarter.frequency'].sudo().search([
            ('partner_id', '=', partner_id),
            ('year', '=', year)
        ])
        if records: return True
        for index in range(1, 5):
            vals = {
                "name": f"Trimestre {index}",
                "year": year,
                "frequencyNumber": 0,
                "partner_id": partner_id
            }
            self.env['quarter.frequency'].sudo().create(vals)
        return True

# class FrequencyLine(models.Model):
#     _name = "res.partner.frequency.line"
#     _description = "Customer Frequence"
#     _inherit = ["mail.thread", "mail.activity.mixin"]

# date_rdv = fields.Datetime(string="Date")
# customer_id = fields.Many2one("res.partner", string="Customer Lines")
# state = fields.Selection(
#     [
#         ("draft", "Draft"),
#         ("plan", "Plan Tournée"),
#         ("programmed", "Programmed"),
#         ("visited", "Visted"),
#         ("late", "Late"),
#     ],
#     default="plan",
# )
# line_note = fields.Html(string="Note")

# days_since_date = fields.Char(
#     string="Elaps Time", compute="_compute_days_since_date"
# )

# @api.model
# def action_draft(self):
#     for rec in self:
#         rec.state = "draft"

# @api.model
# def action_programmed(self):
#     for rec in self:
#         rec.state = "programmed"

# @api.model
# def action_visited(self):
#     for rec in self:
#         rec.state = "visited"

# @api.model
# def action_late(self):
#     for rec in self:
#         rec.state = "late"

# create frequence

# for product in self:
#     existing_bom = self.env["mrp.bom"].search(
#         [("product_tmpl_id", "=", self.product_tmpl_id.id)], limit=1
#     )

#     if not existing_bom:

#         if self.product_tmpl_id:
#             # Créer la nomenclature (BOM)
#             bom = self.env["mrp.bom"].create(
#                 {
#                     "product_tmpl_id": self.product_tmpl_id.sudo().id,  # Utilise l'ID du modèle de produit
#                     "product_qty": 1,  # Quantité de nomenclature
#                     "type": "normal",  #'normal' (standard) ou 'phantom' (kit)
#                     "code": "teste",  # refernce nomenclature
#                 }
#             )
#         # Paramètres fictifs pour l'exemple
#         # Créer les lignes de nomenclature (BOM Lines)
#         for line in self.listeOptions:
#             print("line xxxxxxxxxxxxxxxxxxxxxxxxxx", line)
#             self.env["mrp.bom.line"].create(
#                 {
#                     "bom_id": bom.id,
#                     "product_id": line.id,  # ID du produit composant
#                     "product_qty": 2,  # Quantité du composant
#                 }
#             )
#         return bom
#     else:
#         print(f"Le produit {product.name} possède déjà une nomenclature (BOM).")

# @api.depends("date_rdv")
# def _compute_days_since_date(self):
#     delta = 0
#     for rec in self:
#         # if rec.date_rdv:
#         today = datetime.now()
#         delta = rec.date_rdv
# print(rec.date_rdv)
# print(delta)
# rec.days_since_date = delta
# print(delta)
# if delta.days == -1:
#     rec.days_since_date = "Aujourd'hui"  # =0
#     # rec.state = "late"
# else:
#     rec.days_since_date = f"{delta.days} jours"
# print(today)
# print(delta)

# code_posfiscale = fields.Selection(_get_posfiscale, string="Position Fiscale")

# wilaya_zone = fields.Char(related="customer_wilaya.zone", string="Zone")


# check mobile unique
_sql_constraints = [
    ("mobile_unique", "unique(mobile)", "Mobile must be unique"),
]

# @api.constrains("mobile")
# def _check_mobile(self):
#     for rec in self:
#         if rec.mobile and len(rec.mobile) != 10:
#             raise ValidationError(_("Mobile must be 10 digits"))

# ovveride create method


# def unlink(self):
#     res = super().unlink()
#     return res
