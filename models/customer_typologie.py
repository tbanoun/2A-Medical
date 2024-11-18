from odoo import models, fields


class CustomerTypologie(models.Model):
    _name = "customer.typologie"
    _description = "Typolgie de prescription"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = "name"

    name = fields.Char(string="Name")
    description = fields.Char(string="Code")
