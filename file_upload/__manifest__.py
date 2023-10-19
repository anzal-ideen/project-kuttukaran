{''
 'name': 'File Upload',
 'summary': """Custom for ERP""",
 'version': '0.1',
 'sequence': '-11111',
 'description': """Custom for ERP""",
 'author': 'Ideenkreise Tech Pvt Ltd',
 'company': 'Ideenkreise Tech Pvt Ltd',
 'website': 'https://www.ideenkreisetech.com',
 'category': 'Tools',
 'depends': ['sale', 'purchase', 'base','stock','mail'],
 'license': 'AGPL-3',
 'data': [
     'data/sequence.xml',
     'security/ir.model.access.csv',
     'views/view.xml',
     'views/menu.xml',
     'views/res_config_settings_views.xml',


 ],

'qweb': [
    # 'static/src/xml/amazone_dashboard.xml',
],
# 'js': [
#     'static/src/js/custom_dashboard.js',
# ],

'assets': {
        'web.assets_backend': [
            # 'file_upload/static/src/xml/custom_dashboard.xml',
            # 'file_upload/static/src/js/amazon_dashboard.js',
        ]
    },


 'demo': [],
 'installable': True,
 'auto_install': False,
 'application': True
 }
