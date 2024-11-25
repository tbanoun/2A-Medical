# -*- coding: utf-8 -*-
from requests.compat import basestring

from odoo import models, fields, api, _
from psycopg2 import errors
from odoo.exceptions import UserError
from odoo.exceptions import AccessError
from datetime import datetime
from odoo.exceptions import ValidationError
import xlwt
import base64
from io import BytesIO


class ResPartner(models.Model):
    _name = "res.partner"
    _inherit = "res.partner"

    ref = fields.Char(string="Code Tiers", default="New", readonly=True)
    sponsored_by = fields.Many2many('res.partner', string="Parrainer par", compute="getAllSponredPartner")
    parrinage_id = fields.Many2one('res.partner', string='Related Company', index=True)
    sponsorship = fields.Many2many('res.partner', 'res_partner_sponsorship_rel', 'parrinage_id', string='Parrainage')
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
                rec.parrinage_id = partner_ids.ids[0]

            else:
                rec.sponsored_by = []
                rec.parrinage_id = None

    @api.model
    def update_presence_status(self, status):
        try:
            self.env["bus.presence"].write({"status": status})
        except errors.SerializationFailure:
            # Réessayer l'opération
            self.update_presence_status(status)

    # incrementer ref
    def create(self, vals_list):
        if "phone" in vals_list:
            phone = vals_list['phone']
            partner = self.env['res.partner'].sudo().search([
                ('phone', '=', phone)
            ])
            if partner: raise ValidationError(
                _('Erreur!, vous ne pouvez pas créer un contact avec un numéro de télephone'
                  'qui est déja utulisé par un autre!'))
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
        if "phone" in vals:
            phone = vals['phone']
            partner = self.env['res.partner'].sudo().search([
                ('phone', '=', phone)
            ])
            if partner: raise ValidationError(
                _('Erreur!, vous ne pouvez pas enregistrer les modifications'
                  'le numéro de télephone est déja utulisé par un autre contact!'))
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

    def import_report_frequency(self):
        """Open the timesheet view for the project"""
        action = self.env['ir.actions.act_window']._for_xml_id(
            'contacts_dnd.act_open_wizard_import_file_xls_frequency')
        return action

    # create function to generate a files xls:
    def generate_report_frequency(self):
        active_ids = self.env.context.get('active_ids', [])
        partner_ids = self.env['res.partner'].sudo().browse(active_ids)
        # Création du classeur et de la feuille de calcul
        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet('frequency contact')
        # Styles
        title_style = xlwt.easyxf('font: bold 1, height 280; align: vert centre, horiz center;' 'pattern: pattern solid, fore_colour grey25;')
        title_sous_style = xlwt.easyxf(
            'font: bold on, height 260, color red; '
            'align: vert centre, horiz left; '
            'pattern: pattern solid, fore_colour yellow;'
        )

        style_text_red = xlwt.easyxf(
            'font: bold on, color red; '
            'align: horiz left; '
            'pattern: pattern solid, fore_colour yellow; '
        )

        style_text_red_right = xlwt.easyxf(
            'font: bold on, color red; '
            'align: horiz right; '
            'pattern: pattern solid, fore_colour yellow; '
        )

        # Définir les styles avec bordure et fond gris clair
        header_style_readonly = xlwt.easyxf(
            'font: bold on, color black; '
            'borders: left thin, right thin, top thin, bottom thin; '
            'align: horiz left; '
            'pattern: pattern solid, fore_colour grey25; '
        )
        header_style = xlwt.easyxf(
            'font: bold on, color black; '
            'borders: left thin, right thin, top thin, bottom thin; '
            'align: horiz center; '
            'pattern: pattern solid, fore_colour green; '
        )
        # get year now
        year = datetime.now().year
        # Titre principal
        sheet.write_merge(0, 1, 0, 9, f"Fiches des fréquences trimestrielles pour l'année - {year}", title_style)
        # la remarque:
        sheet.write_merge(2, 2, 0, 9, f"Remarques:", title_sous_style)
        sheet.write_merge(3, 4, 0, 5, f"1.Vous pouvez uniquement modifier les cases dans l'arrière-plan de couleur verte.", style_text_red)
        sheet.write_merge(5, 6, 0, 5, f"2.Les cases dans l'arrière-plan gris sont réservées à l'administration.", style_text_red)
        sheet.write_merge(7, 7, 0, 5, "", style_text_red)
        #les required
        sheet.write_merge(3, 3, 6, 9, f"Type de fréquence:", title_sous_style)
        sheet.write_merge(4, 4, 6, 6, f"1  =>", style_text_red_right)
        sheet.write_merge(4, 4, 7, 9, f"Semaine (Week)", style_text_red)
        sheet.write_merge(5, 5, 6, 6, f"2  =>", style_text_red_right)
        sheet.write_merge(5, 5, 7, 9, f"Mois (Month)", style_text_red)
        sheet.write_merge(6, 6, 6, 6, f"3  =>", style_text_red_right)
        sheet.write_merge(6, 6, 7, 9, f"Quart (Quarter)", style_text_red)
        sheet.write_merge(7, 7, 6, 9, f"", title_sous_style)
        # Largeur totale définie par le tableau principal (10 colonnes)
        total_width = 256 * 20 * 10  # Exemple: chaque colonne principale a une largeur de 20 caractères
        # Largeur totale définie par le tableau principal (10 colonnes)
        total_width = 256 * 20 * 10  # Exemple: chaque colonne principale a une largeur de 20 caractères

        # Calculer la largeur par colonne
        width_per_col_main = total_width // 10  # Largeur par colonne du tableau principal
        width_per_col_small = total_width // 4  # Largeur par colonne pour le tableau à 4 colonnes

        # Ajuster la largeur des colonnes du premier tableau (4 colonnes)
        for col_index in range(4):  # Le premier tableau a 4 colonnes
            sheet.col(col_index).width = width_per_col_small

        # Ajuster la largeur des colonnes du deuxième tableau (10 colonnes)
        for col_index in range(0, 10):  # Le deuxième tableau a 10 colonnes
            if col_index == 0:
                sheet.col(col_index).width = width_per_col_main // 6
                continue
            sheet.col(col_index).width = width_per_col_main
        index = 10
        for partner in partner_ids:
            # Informations de contact sous forme de tableau
            sheet.write_merge(index, index, 0, 1, f"ID", header_style_readonly)
            sheet.write_merge(index, index, 2, 3, f"Nom & prénom: {partner.name}", header_style_readonly)
            sheet.write_merge(index, index, 4, 6, f"Email: {partner.email}", header_style_readonly)
            sheet.write_merge(index, index, 7, 9, f"Télephone: {partner.phone}", header_style_readonly)
            records = self.env['quarter.frequency'].sudo().search([
                ('partner_id', '=', partner.id),
                ('year', '=', year)
            ])
            if not records:
                partner._createRecordQuarter(partner.id)
                records = self.env['quarter.frequency'].sudo().search([
                    ('partner_id', '=', partner.id),
                    ('year', '=', year)
                ])
            index += 1
            for el in records:
                # insert tableau des trimestre
                sheet.write_merge(index, index, 0, 1, f"{partner.id}", header_style_readonly)
                sheet.write_merge(index, index, 2, 3, f"{el.name}", header_style_readonly)
                sheet.write_merge(index, index, 4, 5, f"Nombre de fréquences", header_style_readonly)
                sheet.write_merge(index, index, 6, 6, f"{el.frequencyNumber or 0}", header_style)
                sheet.write_merge(index, index, 7, 8, f"Type de fréquence", header_style_readonly)
                sheet.write_merge(index, index, 9, 9, f"{el.code_type_freq or '0'}", header_style)
                index += 1
            index += 2

        # Enregistrement dans un flux BytesIO
        fp = BytesIO()
        workbook.save(fp)
        fp.seek(0)
        xls_data = fp.read()
        fp.close()

        # Création d'une pièce jointe pour le téléchargement
        attachment = self.env['ir.attachment'].create({
            'name': f'Fiches des fréquences trimestrielles{year}.xls',
            'type': 'binary',
            'datas': base64.b64encode(xls_data),
            'store_fname': f'Fiches_des_frequences_trimestrielles{year}.xls',
            'mimetype': 'application/vnd.ms-excel',
        })

        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/%s?download=true' % attachment.id,
            'target': 'self',
        }


# check mobile unique
_sql_constraints = [
    ("mobile_unique", "unique(mobile)", "Mobile must be unique"),
]


class FrequencyFileXls(models.Model):
    _name = "file.xls"

    file_xls = fields.Binary("File xls")
    trimstre = fields.Selection(
        [
            ('Trimestre 1', 1),
            ('Trimestre 2', 2),
            ('Trimestre 3', 3),
            ('Trimestre 4', 4)
        ], string='Usage',
        default=1, required=True)
