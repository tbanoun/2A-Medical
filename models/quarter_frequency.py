from odoo import fields, models, api

class QuarterFrequency(models.Model):
    _name = "quarter.frequency"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    @api.model
    def _get_type_freq(self):
        selection = []
        for emp in self.env["type.freq"].search([]):
            selection += [("%s" % emp.id, "%s" % emp.description)]
        return selection

    name = fields.Char("Trimestre")
    year = fields.Integer("Années")
    frequencyNumber = fields.Integer("Frequency number")
    partner_id = fields.Many2one("res.partner")
    code_type_freq = fields.Selection(_get_type_freq, string="Frequency")

