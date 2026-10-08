from odoo import models, fields

class TailorPantStyle(models.Model):
    _name = 'tailor.pant.style'
    _description = 'Pant Style Master'
    _rec_name = 'name'

    name = fields.Char(string="Pant Style Name", required=True)
    code = fields.Char(string="Style Code")
    description = fields.Text(string="Description")

    # Optional fields
    waist_type = fields.Selection([
        ('normal', 'Normal Waist'),
        ('high', 'High Waist'),
        ('low', 'Low Waist'),
    ], string="Waist Type")

    fit_type = fields.Selection([
        ('regular', 'Regular Fit'),
        ('slim', 'Slim Fit'),
        ('skinny', 'Skinny Fit'),
        ('loose', 'Loose Fit'),
    ], string="Fit Type")