from odoo import api, fields, models

class EventEvent(models.Model):
    _inherit = "event.event"


    famille = fields.Many2one('event.tag.category', string="Famille")