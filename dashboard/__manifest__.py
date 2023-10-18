{''
 'name': 'Custom Dashboard',
 'summary': """Custom for ERP""",
 'version': '0.1',
 'sequence': '-99991',
 'description': """Custom for ERP""",
 'author': 'Ideenkreise Tech Pvt Ltd',
 'company': 'Ideenkreise Tech Pvt Ltd',
 'website': 'https://www.ideenkreisetech.com',
 'category': 'Tools',
 'depends': ['sale', 'base_accounting_kit', 'purchase', 'base', 'stock', 'vendor_portal', 'board', 'product_purchase',
             'vendor_po','web','board'],
 'license': 'AGPL-3',
 'data': [

     # 'views/view.xml',
     'views/menu.xml',

 ],
 'qweb':['static/src/xml/dashboard.xml'],

 # 'assets': {
 #     'web.assets_backend': [
 #         "dashboard/static/src/js/dashboard.js",
 #
 #     ]},
 #     'web.assets_qweb': [
 #         'project_dashboard_odoo/static/src/xml/dashboard.xml',
 #
 #     ],
 # },

 'demo': [],
 'installable': True,
 'auto_install': False,
 'application': True
 }
