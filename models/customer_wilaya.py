from odoo import models, fields


class Wilaya(models.Model):
    _name = "customer.wilaya"
    _description = "_Wilaya"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = "name"

    name = fields.Char(string="Wilaya")
    code = fields.Char(string="Code Wilaya")
    country_id = fields.Integer(string="Code Pays")
