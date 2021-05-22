# -*- coding: utf-8 -*-
# from odoo import http


# class InvBankStatement(http.Controller):
#     @http.route('/inv_bank_statement/inv_bank_statement/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/inv_bank_statement/inv_bank_statement/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('inv_bank_statement.listing', {
#             'root': '/inv_bank_statement/inv_bank_statement',
#             'objects': http.request.env['inv_bank_statement.inv_bank_statement'].search([]),
#         })

#     @http.route('/inv_bank_statement/inv_bank_statement/objects/<model("inv_bank_statement.inv_bank_statement"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('inv_bank_statement.object', {
#             'object': obj
#         })
