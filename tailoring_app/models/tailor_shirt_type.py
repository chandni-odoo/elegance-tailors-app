from odoo import models, fields

class TailorShirtType(models.Model):
    _name = 'tailor.shirt.type'
    _description = 'Shirt Type Master'
    _rec_name = 'name'

    name = fields.Char(string="Shirt Type Name", required=True)
    code = fields.Char(string="Code")
    price = fields.Float(string="Price")
    description = fields.Text(string="Description")

    fit_type = fields.Selection([
        ('regular', 'Regular Fit'),
        ('slim', 'Slim Fit'),
        ('skinny', 'Skinny Fit'),
        ('loose', 'Loose Fit'),
    ], string="Fit Type")

    sleeve_type = fields.Selection([
        ('full', 'Full Sleeve'),
        ('half', 'Half Sleeve'),
        ('rollup', 'Roll-Up Sleeve'),
    ], string="Sleeve Type")

    collar_type = fields.Selection([
        ('regular', 'Regular Collar'),
        ('chinese', 'Chinese Collar'),
        ('mandarin', 'Mandarin Collar'),
        ('cutaway', 'Cutaway Collar'),
    ], string="Collar Type")
