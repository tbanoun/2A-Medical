from datetime import datetime
from odoo import models, fields, api, _


class Crmlead(models.Model):
    _name = "crm.lead"
    _inherit = ["crm.lead", "mail.thread", "mail.activity.mixin", "utm.mixin"]

    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("canceled", "Canceled"),
        ]
    )

    partner_id = fields.Many2one(
        "res.partner",
    )
    # domain=lambda self: self._find_user(), store=True
    # partner_id = fields.Many2one("res.partner", required=True)

    zone_partner = fields.Char(
        string="Zone Client", related="partner_id.zone", readonly=True, store=True
    )

    # @api.depends("id_partner")
    # def _compute_current_zone_partner(self):
    #     for record in self:
    #         if record.id_partner:
    #             # Vérification de l'existence du champ 'zone' dans le modèle res.partner
    #             record.zone_partner = record.id_partner.zone or "Zone non définie"
    #             print("Zone :", record.zone_partner)
    #         else:
    #             print("Aucun partenaire sélectionné")
    #             record.zone_partner = "Aucun partenaire sélectionné"

    user_id_duo = fields.Many2many("res.users", string="Duo User")
    visite_date_from = fields.Datetime(
        string="Visite From",
        tracking=True,
    )
    default = (datetime.now(),)
    visite_date_to = fields.Datetime(
        string="Visite To",
        tracking=True,
    )

    message_fort = fields.Html(string="Message Fort")

    code_visit_next = fields.Html(
        string="Objectif",
        help="Objectif de la prochaine visite visite",
    )
    code_visite_objection = fields.Html(
        string="Objection",
        help="Les objections relatives à cette visite",
    )

    code_product = fields.Many2many(
        "product.template",
        string="Poduct",
        help="Les produits discutées au moment de la visite",
    )
    canal_visite = fields.Selection(
        [
            ("face2face", "Face to Face"),
            ("mail", "Email"),
            ("sms", "SMS"),
            ("whatsapp", "Whatsapp"),
            ("viber", "Viber"),
            ("linkedIn", "LinkedIn"),
        ],
        default="face2face",
        string="Canal Visite",
    )

    interet_customer = fields.Selection(
        [("positive", "Positive"), ("negative", "Negative")],
        default="positive",
        string="Interet Customer",
    )

    besoin_particulier = fields.Html(string="Besoin particulier")

    point_accord = fields.Html(string="Point d'accord")

    product_presented = fields.Many2many(
        "product.product",
        "crm_lead_product_presented_rel",
        "crm_lead_id",
        "product_id",
        string="Produit présenté",
    )
    product_echant = fields.Many2many(
        "product.product",
        "crm_lead_product_echant_rel",
        "crm_lead_id",
        "product_id",
        string="Echantillion",
    )
    product_discount = fields.Many2many(
        "product.product",
        "crm_lead_product_discount_rel",
        "crm_lead_id",
        "product_id",
        string="Discount Product",
    )
    remis = fields.Many2many(
        "crm.visit.remis",
        string="Remis",
    )

    point_accord = fields.Html(string="Point d’accord")

    invitation = fields.Html(string="Invitation")
    events_id = fields.Many2many("event.event", string="Events")
    events_dates = fields.Char(string="Event Dates", compute="_compute_event_dates")
    typo_prescription = fields.Html(string="Typologie de prescription")

    type_person = fields.Boolean(related="partner_id.is_company")
    wilaya_id = fields.Many2one('customer.wilaya', related="partner_id.wilaya_id", store=True)
    commune_id = fields.Many2one('customer.commune', related="partner_id.commune_id", store=True)
    locality_id = fields.Many2one('customer.locality', related="partner_id.locality_id", store=True)
    zone = fields.Char(related="partner_id.zone", store=True)
    code_potential = fields.Selection(related="partner_id.code_potential")
    code_adoption = fields.Selection(related="partner_id.code_adoption")
    code_solvency = fields.Selection(related="partner_id.code_solvency")
    code_sector = fields.Selection(related="partner_id.code_sector")
    code_leader = fields.Many2many('customer.leader', related="partner_id.code_leader")
    code_category = fields.Many2one('customer.category', related="partner_id.code_category")
    code_typologie = fields.Many2many('customer.typologie', related="partner_id.code_typologie")

    @api.depends("events_id")
    def _compute_event_dates(self):
        for record in self:
            dates = []
            for event in record.events_id:
                if event.date_begin:
                    dates.append(
                        event.date_begin.strftime("%Y-%m-%d")
                    )  # Adjust the format as needed
            record.events_dates = ", ".join(dates) if dates else "No Dates"

    # def action_cancel(self):
    #     return self.write({"state": "canceled"})

    # recuperere users
    # @api.depends()
    # def _find_user(self):
    #     current_user = self.env.user
    #     user_domain = getattr(current_user, "user_domain", False)
    #     print("user_domain", user_domain)
    #     return user_domain

    # create a new lead
    # @api.model
    # def action_create_lead(self):
    #     print("teste")
    #     # recuperer l'ensemble des clients de cette user
    #     # verifie si il a des opportinite
    #     # convertir la frequence
    #     current_user = self.env.user
    #     user_domain = getattr(current_user, "user_domain", False)
    #     print("user_domain", user_domain)
    #     partner_ids = [12373, 12374, 12375, 12376, 12377]
    #     leads = []
    #     for partner_id in partner_ids:
    #         partner = self.env["res.partner"].browse(
    #             partner_id
    #         )  # Récupère l'objet partenaire

    #         if partner:  # Vérifie si le partenaire existe
    #             print("recoooooooooooo", partner.name)  # Affiche le nom du partenaire

    #         # Crée un nouvel enregistrement dans 'crm.lead'
    #         new_lead = self.env["crm.lead"].create(
    #             {
    #                 "name": "Nouvelle Opportunité %s"
    #                 % partner.name,  # Utilise le nom du partenaire
    #                 "partner_id": partner_id,
    #                 "email_from": partner.email
    #                 or "client@example.com",  # Utilise l'email du partenaire si disponible
    #                 "phone": partner.phone
    #                 or "0123456789",  # Utilise le téléphone du partenaire si disponible
    #                 "description": "Ceci est une description pour une nouvelle opportunité",
    #                 "type": "opportunity",
    #             }
    #         )
    #     leads.append(new_lead)  # Ajoute chaque lead créé dans la liste

    #     return leads

    # @api.model
    def write(self, vals):
        # Si le stage_id change (par exemple avec le drag-and-drop dans le kanban)
        if "stage_id" in vals:
            # Effectuer des actions supplémentaires, par exemple changer une priorité
            if vals["stage_id"] == 2:  # remplacez par votre logique
                vals.update({"visite_date_from": "2024-10-10"})
            if vals["stage_id"] == 1:  # remplacez par votre logique
                vals.update({"visite_date_from": "", "priority": "0"})
            return super(Crmlead, self).write(vals)