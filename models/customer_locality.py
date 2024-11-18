from odoo import models, fields


class Locality(models.Model):
    _name = "customer.locality"
    _description = "_locality"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = "name"

    name = fields.Char(string="Name")
    code = fields.Char(string="Code")
    wilaya_id = fields.Char(string="Wilaya")
    wilaya_name = fields.Char()
