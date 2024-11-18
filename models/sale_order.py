# -*- coding: utf-8 -*-

from datetime import datetime
from email.policy import default
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _name = "sale.order"
    _inherit = "sale.order"
