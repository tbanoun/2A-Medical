from odoo import models, fields, api


class Function(models.Model):
    _name = "customer.function"
    _description = "Job Function"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = "name"

    name = fields.Char(string="Name", required=True)
    description = fields.Char(string="Description")
    date_function = fields.Date(string="Date jobs")

    @api.model
    def create(self, vals):
        if "name" in vals:
            vals["name"] = vals[
                "name"
            ].upper()  # Convertir en majuscule lors de la création
        return super(Function, self).create(vals)

    @api.onchange("name")
    def _onchange_name(self):
        if self.name:
            self.name = self.name.upper()
