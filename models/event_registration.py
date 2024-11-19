from odoo import models, api, fields

class EventRegistration(models.Model):
    _inherit = 'event.registration'
    resrvedBy = fields.Many2one('hr.employee', string="Réservé par")
    partner_id = fields.Many2one("res.partner", string="Participant")
    name = fields.Char(related="partner_id.name")
    email = fields.Char(related="partner_id.email")
    phone = fields.Char(related="partner_id.phone")