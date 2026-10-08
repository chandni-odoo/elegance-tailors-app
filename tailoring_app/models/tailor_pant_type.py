from odoo import models, fields

class TailorPantType(models.Model):
    _name = 'tailor.pant.type'
    _description = 'Pant Type Master'
    _rec_name = 'name'

    name = fields.Char(string="Pant Type", required=True)
    code = fields.Char(string="Code")
    price = fields.Float(string="Price")

    description = fields.Text(string="Description")
