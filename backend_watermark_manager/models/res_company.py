from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    watermark_image = fields.Binary(string="Watermark Image")

