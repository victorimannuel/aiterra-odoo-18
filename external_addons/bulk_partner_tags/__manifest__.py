{
    'name': 'Bulk Add Partner Tags',
    'version': '0.1',  
    'summary': 'Wizard to add tags to multiple contacts in bulk',
    'author': 'Your Company',
    'category': 'Tools',
    'license': 'LGPL-3',
    'depends': ['contacts'],  
    'data': [
        'security/ir.model.access.csv',
        'views/wizard_add_tags_view.xml',
        'views/server_action.xml',
    ],
    'installable': True,
    'application': False,
}