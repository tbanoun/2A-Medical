from odoo import models, fields, api


class Commune(models.Model):
    _name = "customer.commune"
    _description = "_Commune"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = "name"

    name = fields.Char(string="Name")
    code = fields.Char(string="Code")
    wilaya_id = fields.Char(string="Wilaya")
    zone = fields.Char(string="Zone")
