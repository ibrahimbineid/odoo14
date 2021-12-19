# -*- coding: utf-8 -*-
{
    'name': "HelpDesk Customization",

    'summary': """
       Make a HelpDesk Customization""",

    'description': """
       Make a HelpDesk Customization
    """,

    'author': "Viltco",
    'website': "https://viltco.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'helpdesk',
    'version': '14.0.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'helpdesk', 'stock', 'maintenance', 'helpdesk_updates', 'website_helpdesk_form', 'website_helpdesk'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/product_views.xml',
        'views/helpdesk_views.xml',
        'views/maintenance_views.xml',
        'views/request.xml',
        'views/site_type.xml',
        'views/optical_test_view.xml',
        'views/attenuation_test_view.xml',
        'views/petrolling_views.xml',
        'reports/report.xml',
        'reports/request_report.xml',
        'reports/helpdesk_report.xml',
        'reports/maintenance.xml',
        'templates/helpdesk_template.xml',
        'data/sequence.xml',
    ],

}
