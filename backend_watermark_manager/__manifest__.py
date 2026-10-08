{
    "name": "Backend Watermark Manager",
    "version": "18.0.1.0.0",
    "category": "Web",
    "summary": "Upload and display a company watermark image across all backend pages.",
    "description": """
Backend Watermark Manager
=========================

This module allows each company to upload a watermark image in the company form.  
Once uploaded, the image is displayed as a background watermark across all backend pages in Odoo.

Key Features:
-------------
- Adds a watermark image field in the Company form  
- Displays the uploaded image as a watermark on all backend pages  
- Company-specific watermark support  
- Simple and lightweight implementation  

Ideal for organizations that want consistent branding or secure watermarking in Odoo’s backend.
    """,
    "author": "TaraXCode Private Limited",
    "company": "TaraXCode Private Limited",
    "website": "https://www.taraxcode.com",
    "depends": ["web", "base"],
    "data": [
        "views/assets.xml",
        "views/res_company_views.xml"
    ],
    "assets": {
        "web.assets_backend": [
            "/backend_watermark_manager/static/src/css/watermark.css"
        ]
    },
    "license": "LGPL-3",
    "installable": True,
    "application": False,
    "auto_install": True,
}
