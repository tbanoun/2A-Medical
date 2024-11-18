from odoo import models, fields, api


class Zone(models.Model):
    _name = "customer.zone"
    _description = "Country State Zone"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = "name"

    name = fields.Char(string="Name")
    description = fields.Char(string="Code")
