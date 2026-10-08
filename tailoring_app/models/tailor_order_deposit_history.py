from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime

class DepositHistory(models.Model):
    _name = 'tailor.order.deposit.history'
    _description = 'Tailor Order Deposit History'

    name = fields.Char(string="Payment Name", readonly=True)
    order_id = fields.Many2one('tailor.order', string='Order',)
    customer_id = fields.Many2one('tailor.customer', string='Customer Name',)
    phone = fields.Char(string="Phone")
    date = fields.Datetime(string='Payment Date', default=fields.Datetime.now)
    amount = fields.Float(string='Deposit Amount',)
    notes = fields.Char(string='Notes')
    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)
    payment_type = fields.Selection([
        ('deposit', 'Deposit'),
        ('delivery', 'Delivery Payment'),
        ('full', 'Full Payment'),
        ('partial', 'Partial Payment'),
        ('refund', 'Refund'),
    ], string="Payment Type", required=True, default='deposit')
    type = fields.Selection([
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('online', 'Online Transfer'),
    ], string="Payment Type", required=True, default='cash')

    def create(self, vals):
        today = datetime.today().strftime('%Y-%m-%d')
        seq = self.env['ir.sequence'].next_by_code('tailor.deposit.seq') or '000'
        vals['name'] = f"ET-INV/{today}/{seq}"
        return super(DepositHistory, self).create(vals)

    def unlink(self):
        raise ValidationError("You cannot delete deposit history!")


    def action_lift_deposit_receipt(self):
        self.ensure_one()
        [data] = self.read()
        active_ids = self.env.context.get('active_ids', [])
        datas = {
            'ids': active_ids,
            'model': 'tailor.order.deposit.history',
            'form': data,
        }

        return self.env.ref('tailoring_app.action_deposit_receipt_pdf').with_context(
            active_ids=self.ids
        ).report_action(self, data=datas)