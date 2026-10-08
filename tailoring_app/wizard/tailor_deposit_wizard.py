from odoo import models, fields

class TailorDepositWizard(models.TransientModel):
    _name = 'tailor.deposit.wizard'
    _description = 'Deposit Wizard'

    order_id = fields.Many2one('tailor.order', string="Order")
    customer_id = fields.Many2one('tailor.customer', string='Customer Name',)
    total_amount = fields.Float(string="Total Amount", readonly=True)
    deposit_amount = fields.Float(string="Deposit Amount", required=True)
    notes = fields.Char(string="Notes")
    type = fields.Selection([
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('online', 'Online Transfer'),
    ], string="Payment Type", required=True, default='cash')

    def action_confirm_deposit(self):
        order = self.order_id

        self.env['tailor.order.deposit.history'].create({
            'order_id': order.id,
            'customer_id': order.customer_id.id,
            'phone': order.customer_id.phone,
            'amount': self.deposit_amount,
            'notes': self.notes,
            'payment_type': "deposit",
            'type': self.type,
        })
        order.deposit_amount += self.deposit_amount
        return {'type': 'ir.actions.act_window_close'}
