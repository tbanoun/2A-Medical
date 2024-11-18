from odoo import models, fields, api


class VisitObjection(models.Model):
    _name = "crm.visit.objection"
    _description = "Objection Visit"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Name")
    description = fields.Char(string="Description")
