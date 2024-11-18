from odoo import models, fields, api


class VisiteDetails(models.Model):
    _name = "crm.visit.details"
    _description = "CRM Detail Visite"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Name")
    description = fields.Char(string="Description")


class VisiteObjection(models.Model):
    _name = "crm.visit.objection"
    _description = "Next Visite"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Name")
    description = fields.Char(string="Description")


class VisiteRemis(models.Model):
    _name = "crm.visit.remis"
    _description = "Remis Visite"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Name")
    description = fields.Char(string="Description")
