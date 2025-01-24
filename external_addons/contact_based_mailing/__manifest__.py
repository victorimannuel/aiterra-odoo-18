{
    'name': 'Contact-Based Mailing Lists',
    'version': '0.1',
    'summary': 'Sync mailing lists with contacts',
    'sequence': 10,
    'description': """Automatically sync mailing lists based on contact filters""",
    'category': 'Tools',
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'depends': ['mass_mailing', 'contacts'],
    'data': [
        'security/ir.model.access.csv',
        'views/mailing_list_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}