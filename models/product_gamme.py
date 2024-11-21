from odoo import models, api, fields

class ProductGamme(models.Model):
    _name ='product.gamme'


    name = fields.Char("Nom")