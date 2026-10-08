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
    "name": "Tailoring App",
    "version": "18.0.1.0.1",
    "summary": "Manage tailoring orders (pants & shirts measurements)",
    "description": "Tailoring order management with pant and shirt measurements, customer info, basic bill report.",
    "category": "Custom",
    "author": "TaraXCode Pvt. Ltd",
    "website": "http://taraxcode.com",
    "depends": ["base", "mail"],
    "data": [
        "data/sequence_data.xml",
        "data/tailor_pant_style_data.xml",
        "data/tailor_shirt_type_demo.xml",
        "data/tailor_silayi_type_demo.xml",
        "data/tailor_pant_type_demo.xml",
        "security/ir.model.access.csv",
        "views/tailor_menu.xml",
        "views/tailor_order_views.xml",
        "views/tailor_customer_view.xml",
        "views/tailor_pant_style_view.xml",
        "views/tailor_pant_type_view.xml",
        "views/tailor_shirt_type_view.xml",
        "views/tailor_silayi_type_view.xml",
        "views/tailor_order_deposit_history.xml",
        "wizard/tailor_deposit_wizard_view.xml",
        "wizard/import_wizard_view.xml",
        "reports/tailor_report.xml",
        "reports/report_deposit_recipt.xml",
    ],
    "installable": True,
    "application": True,
    "license": "LGPL-3",
}
