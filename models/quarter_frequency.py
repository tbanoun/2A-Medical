from odoo import fields, models, api

class QuarterFrequency(models.Model):
    _name = "quarter.frequency"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    @api.model
    def _get_type_freq(self):
        selection = []
        for emp in self.env["type.freq"].search([]):
            selection += [("%s" % emp.id, "%s" % emp.description)]
        return selection

    name = fields.Char("Trimestre")
    year = fields.Integer("Années")
    frequencyNumber = fields.Integer("Frequency number")
    partner_id = fields.Many2one("res.partner")
    code_type_freq = fields.Selection(_get_type_freq, string="Frequency")


    def _createCardCrmLead(self, id):
        print("ok id:", id)
        record = self.env['quarter.frequency'].sudo().browse(id)
        print("ok record:", record)
        if not record: return
        id = record.id
        crmLeadNewStage = self.env["crm.lead"].search([
            ("partner_id", "=", record.partner_id.id),
            ("frequency", "=", id),
            ("stage_id.name", "in", ("Nouveau", "New", "new", "nouveau")),
            ("year", "=", record.year)
        ])
        crmLead = self.env["crm.lead"].sudo().search([
            ("partner_id", "=", record.partner_id.id),
            ("frequency", "=", id),
            ("year", "=", record.year)
        ])

        frequence = 0
        if record.code_type_freq == "1": frequence = record.frequencyNumber * 12 # week
        elif record.code_type_freq == "2": frequence = record.frequencyNumber * 3 # month
        elif record.code_type_freq == "3": frequence = record.frequencyNumber # quarter
        if crmLead:
            if len(crmLead) == frequence: return True
        if len(crmLead) > frequence:
            crmLeadNewStage.sudo().unlink()
        elif len(crmLead) < frequence:
            difference_card = frequence - len(crmLead)
            #créer les nouvelle cartes:
            for i in range(0, difference_card):
                self.env["crm.lead"].sudo().create(
                    {
                        "name": "New Lead %s" % record.partner_id.name,
                        "partner_id": record.partner_id.id,
                        "type": "opportunity",
                        "frequency": id,
                        "year": record.year
                    }
                )
                print("Create success !")
        return True

    def create(self, vals_list):
        res = super(self, QuarterFrequency).create(vals_list)
        if 'frequencyNumber' in vals_list and 'code_type_freq' in vals_list:
            self._createCardCrmLead(res.id)
        return res

    def write(self, vals):
        res = super(QuarterFrequency,self).write(vals)
        if 'frequencyNumber' in vals or 'code_type_freq' in vals:
            self._createCardCrmLead(self.id)
        return res