from odoo import fields, models, api
from datetime import datetime

class QuarterFrequency(models.Model):
    _name = "quarter.frequency"
    _inherit = ["mail.thread", "mail.activity.mixin"]


    name = fields.Char("Trimestre")
    year = fields.Integer("Années")
    frequencyNumber = fields.Integer("Frequency number")
    partner_id = fields.Many2one("res.partner")



    def _createRecordQuarter(self, partner_id):
        year = datetime.now().year()
        records = self.env['quarter.frequency'].sudo().search([
            ('partner_id', '=', partner_id),
            ('year', '=', int(year))
        ])
        if records: return True
        for index in range(1, 5):
            vals = {
                "name": f"Trimestre {index}",
                "year": int(year),
                "frequencyNumber": 0,
                "partner_id": partner_id


            }
            self.env['quarter.frequency'].sudo().create(vals)
        return True




