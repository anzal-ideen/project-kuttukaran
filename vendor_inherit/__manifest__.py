{
    'name': 'Vendor Code',
    'version': '1.0.0',
    'category': 'Purchase products',
    'author': 'ideenkreise',
    'sequence': -100,
    'summary': 'purchase management system',
    'description': """product purchase management system""",
    'depends': ['base', 'account', 'hr', 'stock', 'purchase','base_accounting_kit'],
    'data': [
                'views/view.xml',


    ],
    'demo': [],
    'application': True,
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
