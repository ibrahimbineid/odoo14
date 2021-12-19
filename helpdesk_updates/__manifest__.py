# -*- coding: utf-8 -*-
{
    'name': 'Helpdesk Updates',
    'version': '13.0.1',
    'summary': 'Helpdesk Updates',
    'category': 'helpdesk',
    'author': 'Magdy, TeleNoc',
    'description': """
    Helpdesk Updates
    """,
    'depends': ['helpdesk', 'maintenance'],
    'data': [
        'security/ir.model.access.csv',
        'views/city_locations.xml',
        'views/helpdesk_view.xml',
        # 'views/website_ticket.xml',
    ]
}
