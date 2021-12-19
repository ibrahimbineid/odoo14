{
    'name': 'Telenoc Login',
    'summary': 'Telenoc Login Page',
    'description': 'This module for login page.',
    'version': '14.0.1.0.0',
    'author': 'Odoo Team, Telenoc',
    'website': 'http://www.telenoc.org/',
    'license': 'AGPL-3',
    'depends': ['telenoc_login_background'],
    'data': [
        'templates/website_templates.xml',
        'templates/webclient_templates.xml',
    ],
    'qweb': [
    ],
    'installable': True,
    'application': True,
}
