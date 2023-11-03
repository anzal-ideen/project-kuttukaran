# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'project excel',
    'version': '1.0.0',
    'category': 'projects excel',
    'author': 'Ideenkreise',
    'sequence': -111,
    'summary': 'project inherit',
    'description': """project inherit""",
    'depends': ['base', 'project', 'hr', 'base_accounting_kit'],
    'data': [
        'views/tasks.xml',
        'views/project.xml',
    ],
    'demo': [],
    'application': True,
    'installable': True,
    'auto_install': False,
    'assets': {
    },
    'post_init_hook': '',
    'license': 'LGPL-3',
}
