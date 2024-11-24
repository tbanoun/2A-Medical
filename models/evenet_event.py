from odoo import api, fields, models

class EventEvent(models.Model):
    _inherit = "event.event"


    famille = fields.Many2one('customer.category', string="Catégorie")
    budget = fields.Monetary(string="Budget", currency_field='company_currency_id')
    company_currency_id = fields.Many2one(related='company_id.currency_id')
    gamme_id = fields.Many2one('product.gamme', string="Gamme de Produits")


