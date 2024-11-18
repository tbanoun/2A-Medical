from odoo import models, fields


class Typefreq(models.Model):
    _name = "type.freq"
    _description = "Type Frequency"
    _inherit = [
        "mail.thread",
        "mail.activity.mixin",
        "mail.render.mixin",
        "utm.source.mixin",
    ]

    name = fields.Char(string="Name")
    description = fields.Char(string="Description")
