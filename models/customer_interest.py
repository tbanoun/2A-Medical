from odoo import models, fields, api


class Interest(models.Model):
    _name = "customer.interest"
    _description = "Customer interes"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Name")
    description = fields.Char(string="Description")

    state = fields.Selection(
        [("draft", "Draft"), ("confirmed", "Confirmed"), ("canceled", "Canceled")],
        string="Status",
        default="draft",
    )

    def action_draft(self):
        for rec in self:
            rec.state = "draft"

    def action_confirmed(self):
        self.state = "confirmed"

    def action_canceled(self):
        self.state = "canceled"
