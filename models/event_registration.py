from odoo import models, api, fields

class EventRegistration(models.Model):
    _inherit = 'event.registration'

    resrvedBy = fields.Many2one('hr.employee', string="Réservé par")
    partner_id = fields.Many2one("res.partner", string="Participant")
    sponsored_by = fields.Many2many('res.partner', string="Parrainer par", compute="getAllSponredPartner")
    name = fields.Char(related="partner_id.name")
    email = fields.Char(related="partner_id.email")
    phone = fields.Char(related="partner_id.phone")

    @api.depends('partner_id')
    def getAllSponredPartner(self):
        for rec in self:
            partner_ids = self.env['res.partner'].sudo().search([
                ('sponsorship', 'in', [rec.partner_id.id])
            ])
            if partner_ids: rec.sponsored_by = partner_ids.ids
            else: rec.sponsored_by = []

