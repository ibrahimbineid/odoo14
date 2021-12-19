# -*- coding: utf-8 -*-
{
    'name': 'hr_assets_assignation',
    'version': '14.0.1',
    'summary': 'asset_account_request',
    'category': 'hr',
    'author': 'Magdy,TeleNoc',
    'description': """
    asset_account_request
    """,
    'depends': ['base', 'mail', 'hr', 'account_asset'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/asset_request_cron.xml',
        'views/asset_request_sequence.xml',
        'views/asset_account_request.xml',
        'report/employee_assets_report.xml',
        'report/department_clearance_report.xml',
    ]
}
