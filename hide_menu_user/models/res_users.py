# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#  Project    : Tailoring Management System (Elegance Tailors)
#  Module     : TaraXCode Pvt Ltd - Custom Odoo Development
#  File       : models/*.py
#  Copyright  : (C) 2025 TaraXCode Pvt Ltd
#  License    : LGPL-3.0 (GNU Lesser General Public License v3.0)
# -----------------------------------------------------------------------------
#  Author     : Parmjeet Singh
#  Company    : TaraXCode Pvt Ltd
#  Description:
#      This module contains the core business logic, models, and methods for
#      managing tailoring orders, measurement tracking, delivery workflow, and
#      pricing automation. It is designed to enhance operational efficiency
#      through optimized Odoo customization.
#
#      Key Functional Areas:
#          - Customer measurement management
#          - Shirt/Pant style customization
#          - Auto price computation
#          - Order flow & delivery date validation
#          - Notes & tracking support
#
#  NOTE:
#      Please do not remove this header. It ensures proper code ownership,
#      licensing compliance and project traceability.
# -----------------------------------------------------------------------------

from odoo import fields, models, api


class ResUsers(models.Model):

    _inherit = 'res.users'

    def write(self, vals):

        old_hide_menu_map = {record.id: record.hide_menu_ids for record in self}
        res = super(ResUsers, self).write(vals)
        for record in self:
            old_hide_menu_ids = old_hide_menu_map.get(record.id,
                                                     self.env['ir.ui.menu'])

            for menu in record.hide_menu_ids:
                menu.sudo().write({'restrict_user_ids': [(4, record.id)]})


            removed_menus = old_hide_menu_ids - record.hide_menu_ids
            for menu in removed_menus:
                menu.sudo().write({'restrict_user_ids': [(3, record.id)]})
        return res

    def _get_is_admin(self):

        for rec in self:
            rec.is_admin = False
            if rec.id == self.env.ref('base.user_admin').id:
                rec.is_admin = True

    hide_menu_ids = fields.Many2many(
        'ir.ui.menu', string="Hidden Menu",
        store=True, help='Select menu items that need to '
                         'be hidden to this user.')
    is_admin = fields.Boolean(compute='_get_is_admin', string="Is Admin",
                              help='Check if the user is an admin.')


class IrUiMenu(models.Model):

    _inherit = 'ir.ui.menu'

    restrict_user_ids = fields.Many2many(
        'res.users', string="Restricted Users",
        help='Users restricted from accessing this menu.')

    @api.returns('self')
    def _filter_visible_menus(self):

        menus = super(IrUiMenu, self)._filter_visible_menus()

        if self.env.user.has_group('base.group_system'):
            return menus

        return menus.filtered(
            lambda m: self.env.user not in m.restrict_user_ids)
