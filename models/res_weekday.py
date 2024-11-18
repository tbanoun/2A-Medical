from odoo import models, fields, api


class ResPeriode(models.Model):
    _name = "res.periode"
    _description = "Periode"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = "name"

    name = fields.Char(string="Periode")


class ResWeekDay(models.Model):
    _name = "res.weekday"
    _description = "week day"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = "name"

    name = fields.Char(string="Week Day")
