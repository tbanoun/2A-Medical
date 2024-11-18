from odoo import models, fields, api


class VisiteProduct(models.Model):
    _name = "crm.visit.product"
    _description = "Product Visite"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Name")
    description = fields.Char(string="Description")
