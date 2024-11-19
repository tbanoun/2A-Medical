from odoo import models, api, fields

class EventRegistration(models.Model):
    _inherit = 'event.registration'
    resrvedBy = fields.Many2one('hr.employee', string="Réservé par")