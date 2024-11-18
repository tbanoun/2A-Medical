from odoo import models, fields, api


class Category(models.Model):
    _name = "customer.category"
    _description = "Customer Category"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Name", tracking=1)
    description = fields.Char(string="Description", tracking=1)
    company_type = fields.Selection(
        [
            ("individual", "Individual"),
            ("company", "Company"),
        ],
        string="Category Type",
        default="individual",
        store=False,
    )
    is_company = fields.Boolean(string="Is Company", default=False)

    # @api.depends("is_company")
    # def _state_category_type(self):
    #     for rec in self:
    #         if rec.is_company:
    #             rec.company_type = "company"
    #         else:
    #             rec.company_type = "individual"

    # @api.onchange("company_type")
    # def _onchange_company_type(self):
    #     for rec in self:
    #         if rec.company_type == "individual":
    #             rec.is_company = False
    #         elif rec.company_type == "company":
    #             rec.is_company = True

    # def action_draft(self):
    #     for rec in self:
    #         rec.state = "draft"

    # def action_confirmed(self):
    #     for rec in self:
    #         rec.state = "confirmed"

    # def action_canceled(self):
    #     for rec in self:
    #         rec.state = "canceled"

    # def action_transfert(self):
    #     for rec in self:
    #         rec.state = "draft"
