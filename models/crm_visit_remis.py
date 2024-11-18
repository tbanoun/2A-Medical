from odoo import models, fields


class VisitRemis(models.Model):
    _name = "crm.visit.remis"
    _description = "CRM Remis Visit"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Name")
    description = fields.Char(string="Description")
