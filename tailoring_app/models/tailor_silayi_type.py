from odoo import models, fields

class TailorSilayiType(models.Model):
    _name = 'tailor.silayi.type'
    _description = 'Silayi Type Master'
    _rec_name = 'name'

    name = fields.Char(string="Silayi Type", required=True)
    code = fields.Char(string="Code")
    charge_type = fields.Selection([
        ('piece', 'Per Piece'),
        ('meter', 'Per Meter'),
    ], string="Charge Type", default='piece')
    description = fields.Text(string="Description")
