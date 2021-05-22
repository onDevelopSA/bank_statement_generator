# © 2021 onDevelop.SA
# ondevelop.sa@gmail.com
# Autor: Idelis Gé Ramírez

import logging
import ast
from odoo import models, fields, api, _


class AccountBankStatement(models.Model):

    _inherit = 'account.bank.statement'
    _description = 'Inherit for some needed fields.'

    origin_move_id = fields.Many2one('account.move')


class AccountBankStatementLine(models.Model):

    _inherit = 'account.bank.statement.line'
    _description = 'Inherit for some needed fields.'

    origin_payment_move_line_id = fields.Many2one('account.move.line')
