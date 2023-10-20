{
    'name': 'Js Dashboard',
    'summary': """Custom for ERP""",
    'version': '0.1',
    'sequence': -11111,  # Remove quotes to indicate it's an integer
    'description': """Custom for ERP""",
    'author': 'Ideenkreise Tech Pvt Ltd',
    'company': 'Ideenkreise Tech Pvt Ltd',
    'website': 'https://www.ideenkreisetech.com',
    'category': 'Tools',
    'depends': ['sale', 'purchase', 'base', 'stock', 'mail','web'],
    'license': 'AGPL-3',
    'data': [
        'views/dashboard_action.xml',
    ],
    'qweb': [
        'static/src/xml/dashboard.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'custom_dashboard/static/src/js/dashboard.js',
        ],
        'web.assets_qweb': [
            'custom_dashboard/static/src/xml/dashboard.xml',
        ],
    },
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True
}
