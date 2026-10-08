from odoo import models, fields

class TailorCustomer(models.Model):
    _name = 'tailor.customer'
    _description = 'Tailor Customer'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Customer Name", required=True)
    address = fields.Text(string='Customer Address', default="Khamgoan")
    street = fields.Char(string="Street")
    street2 = fields.Char(string="Street 2")
    city = fields.Char(string="City")
    state_id = fields.Many2one('res.country.state', string="State")
    zip = fields.Char(string="ZIP")
    country_id = fields.Many2one('res.country', string="Country")

    phone = fields.Char(string="Phone")
    email = fields.Char(string="Email")

    # Extra fields (Optional)
    notes = fields.Text(string="Notes")
    image_1920 = fields.Image(string="Photo")
