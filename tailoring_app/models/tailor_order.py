from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date, timedelta


class TailorOrder(models.Model):
    _name = 'tailor.order'
    _description = 'Tailoring Order'
    _rec_name = 'display_name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Order Reference', required=True, copy=False, default=lambda self: 'New')
    display_name = fields.Char(string='Display Name', compute='_compute_display_name')
    customer_id = fields.Many2one('tailor.customer',string='Customer Name',required=True, tracking=True,)
    phone = fields.Char(string='Phone')
    address = fields.Text(string='Customer Address', default="Khamgoan")
    street = fields.Char('Street',tracking=True,)
    street2 = fields.Char('Street2', tracking=True,)
    zip = fields.Char('Zip', change_default=True, tracking=True,)
    city = fields.Char('City', tracking=True,)
    state_id = fields.Many2one("res.country.state", string='State',domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one('res.country', string='Country')

    date = fields.Date(string='Order Date', default=fields.Date.context_today)
    delivery_date = fields.Date(string='Delivery Date', required=True, tracking=True,)
    note = fields.Html(string='Note')
    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('cutting', 'Cutting'),
        ('inprogress', 'In Progress'),
        ('iron', 'Iron'),
        ('ready', 'Ready'),
        ('delivered', 'Delivered'),
        ('cancel', 'Cancelled'),
    ], default='draft', tracking=True)

    pant_ids = fields.One2many('tailor.order.pants', 'order_id', string='Pants',)
    shirt_ids = fields.One2many('tailor.order.shirts', 'order_id', string='Shirts',)
    deposit_history_ids = fields.One2many('tailor.order.deposit.history', 'order_id', string='Deposits',)

    pant_qty = fields.Integer(string='Total Pant', readonly=True)
    shirt_qty = fields.Integer(string='Total Shirt', readonly=True)
    total_amount = fields.Float(compute='_compute_total_amount')
    deposit_amount = fields.Float(string="Deposit Amount", default=0.0)
    remaining_amount = fields.Float(compute='_compute_remaining_amount')
    deposit_count = fields.Integer(compute='_compute_deposit_count')

    @api.depends('deposit_history_ids')
    def _compute_deposit_count(self):
        for rec in self:
            rec.deposit_count = len(rec.deposit_history_ids)

    def action_view_deposit(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Deposit History',
            'res_model': 'tailor.order.deposit.history',
            'view_mode': 'list,form',
            'domain': [('order_id', '=', self.id)],
            'context': {'default_order_id': self.id}
        }

    def action_open_deposit_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Add Deposit',
            'res_model': 'tailor.deposit.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_order_id': self.id,
                'default_customer_id': self.customer_id.id,
                'default_total_amount': self.total_amount,
            }
        }

    @api.depends('pant_ids.total_price', 'shirt_ids.total_price','pant_ids.pant_qty','shirt_ids.shirt_qty')
    def _compute_total_amount(self):
        for order in self:
            pant_total = sum(order.pant_ids.mapped('total_price'))
            order.pant_qty = sum(order.pant_ids.mapped('pant_qty'))
            order.shirt_qty = sum(order.shirt_ids.mapped('shirt_qty'))
            shirt_total = sum(order.shirt_ids.mapped('total_price'))
            order.total_amount = pant_total + shirt_total

    @api.depends('total_amount', 'deposit_amount')
    def _compute_remaining_amount(self):
        for order in self:
            order.remaining_amount = order.total_amount - order.deposit_amount

    @api.onchange('delivery_date')
    def _onchange_delivery_date(self):
        if self.delivery_date:
            tomorrow = date.today() + timedelta(days=1)
            if self.delivery_date <= tomorrow:
                self.delivery_date = False
                return {
                    'warning': {
                        'title': _("Invalid Delivery Date"),
                        'message': _(
                            "Delivery Date should be at least from tomorrow onward. Today and past dates are not allowed.")
                    }
                }

    @api.onchange('customer_id')
    def _onchange_customer_id(self):
        if self.customer_id:
            self.address = self.customer_id.address
            self.phone = self.customer_id.phone
        else:
            self.address = False

    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            seq = self.env['ir.sequence'].next_by_code('tailor.order') or 'New'
            vals['name'] = seq
        return super().create(vals)

    @api.depends('name','customer_id')
    def _compute_display_name(self):
        for rec in self:
            if rec.customer_id:
                rec.display_name = f"{rec.name} / {rec.customer_id.name}"
            else:
                rec.display_name = rec.name

    def action_confirm(self):
        self.state = 'confirm'

    def action_cutting(self):
        self.state = 'cutting'

    def action_inprogress(self):
        self.state = 'inprogress'

    def action_iron(self):
        self.state = 'iron'

    def action_ready(self):
        self.state = 'ready'

    def action_delivered(self):
        for order in self:
            if order.remaining_amount > 0:
                raise ValidationError(
                    "Order cannot be delivered because remaining amount is not fully paid."
                )
            order.state = 'delivered'

    def action_cancel(self):
        self.state = 'cancel'

    def action_reset_to_draft(self):
        self.state = 'draft'


    def action_print_pant(self):
        self.ensure_one()
        [data] = self.read()
        active_ids = self.env.context.get('active_ids', [])
        datas = {
            'ids': active_ids,
            'model': 'tailor.order',
            'form': data,
        }
        return self.env.ref('tailoring_app.action_pant_measurement_pdf').with_context(
            active_ids=self.ids
        ).report_action(self, data=datas)

    def action_print_shirt(self):
        self.ensure_one()
        [data] = self.read()
        active_ids = self.env.context.get('active_ids', [])
        datas = {
            'ids': active_ids,
            'model': 'tailor.order',
            'form': data,
        }
        return self.env.ref('tailoring_app.action_shirt_measurement_pdf').with_context(
            active_ids=self.ids
        ).report_action(self, data=datas)


class TailorOrderPant(models.Model):
    _name = 'tailor.order.pants'
    _description = 'Tailoring Order Pant'

    order_id = fields.Many2one('tailor.order', string='Order')
    pant_type_id = fields.Many2one('tailor.pant.type', string='Pant Type', tracking=True, )
    pant_style_id = fields.Many2one('tailor.pant.style', string='Pant Style', tracking=True)
    silai_type_id = fields.Many2one('tailor.silayi.type', string='Silai Type', tracking=True, )
    pant_front_pocket = fields.Selection([('side', 'Side'), ('crose', 'Crose')], string='Front Pocket', tracking=True, )
    pant_back_pocket = fields.Selection([('1', '1'), ('2', '2')], string='Back Pocket', tracking=True, )
    pant_qty = fields.Integer(string='Pant Quantity', default=1, tracking=True)
    pant_price = fields.Float(string='Pant Price', compute='_compute_pant_price', store=True)
    discount = fields.Float(string='Discount %', default=0)
    total_price = fields.Float(string='Total Amount', compute='_compute_pant_price', store=True)
    pant_lambai = fields.Char(string='Lambai', tracking=True, )
    pant_kamar = fields.Char(string='Kamar', tracking=True, )
    pant_sit = fields.Char(string='Sit', tracking=True, )
    pant_jang = fields.Char(string='Jang', tracking=True, )
    pant_bottom = fields.Char(string='Bottom', tracking=True, )
    pant_kistak = fields.Char(string='Kistak', tracking=True, )
    pant_guthna = fields.Char(string='Guthna', tracking=True, )
    notes = fields.Text(string='Notes')

    @api.depends('pant_type_id', 'pant_qty', 'discount')
    def _compute_pant_price(self):
        for rec in self:
            if rec.pant_type_id:
                rec.pant_price = rec.pant_type_id.price
            else:
                rec.pant_price = 0
            amount = rec.pant_qty * rec.pant_price
            if rec.discount > 0:
                amount = amount - (amount * rec.discount / 100)
            rec.total_price = amount


class TailorOrderShirts(models.Model):
    _name = 'tailor.order.shirts'
    _description = 'Tailoring Order Shirts'

    order_id = fields.Many2one('tailor.order', string='Order')
    shirt_style_id = fields.Many2one('tailor.shirt.type', string='Shirt Style', tracking=True, )
    shirt_lambai = fields.Char(string='Lambai', tracking=True, )
    shirt_chati = fields.Char(string='Chati', tracking=True, )
    shirt_shoulder = fields.Char(string='Shoulder', tracking=True, )
    shirt_aastin = fields.Char(string='Aastin', tracking=True, )
    shirt_gala = fields.Char(string='Gala', tracking=True, )
    shirt_peat = fields.Char(string='Peat', tracking=True, )
    shirt_front = fields.Char(string='Front', tracking=True, )
    shirt_patti = fields.Selection([('undar', 'Undar'), ('bahar', 'Bahar')], string='Patti', tracking=True, )
    others = fields.Selection(
        [
            ('double_silai ', 'Double Silai'),
            ('without_pocket', 'Without Pocket'),
        ],
        string='Patti Type',
        tracking=True,
    )
    shirt_collar = fields.Selection([('Choti', 'Choti'), ('Badhi', 'Badhi'), ('Kinar Patti', 'Kinar Patti')], string='Collar', tracking=True, )
    shirt_a = fields.Char(string='A', tracking=True, )
    shirt_qty = fields.Integer(string='Shirt Quantity', default=1, tracking=True)
    shirt_price = fields.Float(string='Shirt Price', compute='_compute_shirt_price', store=True)
    discount = fields.Float(string='Discount %', default=0)
    total_price = fields.Float(string='Total Amount', compute='_compute_shirt_price', store=True)
    notes = fields.Text(string='Notes')

    @api.depends('shirt_style_id', 'shirt_qty', 'discount')
    def _compute_shirt_price(self):
        for rec in self:
            price = rec.shirt_style_id.price if rec.shirt_style_id else 0.0
            qty = rec.shirt_qty or 0
            discount = rec.discount or 0
            rec.shirt_price = price
            total = price * qty
            if discount:
                total -= (total * discount / 100)

            rec.total_price = total