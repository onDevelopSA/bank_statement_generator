# -*- coding: utf-8 -*-
# © 2021 onDevelop.sa
# Autor: Idelis Gé Ramírez
# Part of onDevelop.SA. See LICENSE file for full copyright and licensing details.
{
    'name': "Bank Statement Generator",
    'summary': """Generate Bank Statements from invoices/bills.""",
    'description': """
    Permit generate a bank statement form an invoice/bill or from many
    invoices/bills using the related payments.
    """,
    'author': "onDevelop.SA",
    'website': "http://www.ondevelop.tech",
    'category': 'Accounting/Accounting',
    'category': 'Uncategorized',
    'version': '14.0.1',
    'license': 'LGPL-3',
    'price': 32,
    'currency': 'USD',
    'depends': ['base', 'account'],
    'images': ['static/description/bank_statement_cover.png'],
    'data': [
        'security/ir.model.access.csv',
        'views/account_move.xml',
        'wizard/register_bank_statement.xml'
    ],
    'demo': ['demo/demo.xml'],
    'installable': True,
    'auto_install': False
}
