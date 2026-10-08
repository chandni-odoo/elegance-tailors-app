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
{
    'name': 'Hide Any Menu User Wise',
    'version': '17.0',
    'category': 'Extra Tools',
    'summary': 'Hide Menu, Hide Menu Items, Restrict Menu Items, User-wise Menu Control, Odoo Apps',
    'description': 'Hide any menu item for specific users with easy configuration and access control.',
    'sequence': 3,
    'author': 'TaraXCode Private Limited',
    'maintainer': 'TaraXcode Private Limited',
    'website': 'http://taraxcode.com/',
    'license': 'OPL-1',
    'depends': ['base'],
    'currency': 'USD',
    'license': 'OPL-1',
    'depends': ['base'],
    'data': [
        'views/res_users_views.xml',
    ],
    'images': ['static/description/banner.png'],
    'installable': True,
    'auto_install': False,
    'application': False,
}
