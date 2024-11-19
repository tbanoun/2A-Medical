from odoo import fields, models, api

class QuarterFrequency(models.Model):
    _name = "quarter.frequency"
    _inherit = ["mail.thread", "mail.activity.mixin"]


    name = fields.Char("Trimestre")
    year = fields.Integer("Années")
    frequencyNumber = fields.Integer("Frequency number")
    partner_id = fields.Many2one("res.partner")