from odoo import models, fields, api


class VisiteNext(models.Model):
    _name = "crm.visit.next"
    _description = "CRM Next Visite"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Name")
    description = fields.Char(string="Description")
