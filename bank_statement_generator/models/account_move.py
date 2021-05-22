# © 2021 onDevelop.SA
# ondevelop.sa@gmail.com
# Autor: Idelis Gé Ramírez

import logging
import ast
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class AccountMove(models.Model):
    _inherit = 'account.move'
    _description = 'Inherit for some needed method.'

    @api.depends('banks_statements_ids')
    def _get_bank_states_count(self):
        '''Calculate the count of related bank statement.'''
        for rec in self:
            rec.bank_states_count = len(rec.banks_statements_ids)

    bank_states_count = fields.Integer(compute="_get_bank_states_count")
    banks_statements_ids = fields.One2many('account.bank.statement',
                                           'origin_move_id')

    def get_payments_moves_lines(self):
        '''Find by each move the related payments and return a list with the
        payment account move line.

        '''
        def was_already_reconciled(pay_move_line_id):
            '''Check if the given payment move line was already
            reconciled in other bank statement.

            '''
            return any(self.env['account.bank.statement.line'].search([
                ('origin_payment_move_line_id', '=', pay_move_line_id)]))

        AccountMoveLine = self.env['account.move.line']
        AccountBankStatementLine = self.env['account.bank.statement.line']
        for move in self:
            search_domain = [('payment_id','!=', False),
                             ('ref', '=', move.name)]
            if move.move_type == 'out_invoice':
                search_domain.append(('credit', '>', 0))
            else:
                search_domain.append(('debit', '>', 0))
            payments_moves = AccountMoveLine.search(search_domain)
            if any(payments_moves):
                for payment_line in payments_moves:
                    if not was_already_reconciled(payment_line.id):
                        yield payment_line

    def register_bank_statement(self):
        '''Call the pop up to generate the bank statements.'''
        ctx = self._context.copy()
        if len(self.mapped('partner_id')) > 1:
            msg_error = "The Bank Statement cannot be generated for different"+\
                        " customers."
            raise ValidationError(_(msg_error))
        if 'done_from_butt' in self._context:
            moves_ids = self.ids
        else:
            moves_ids = self._context.get('active_ids')
        info_carrier = self.env['register.bank.statement'].create(
            {'statement_name': 'Bank Statement for {inv}'.format(inv=self.name)})
        ctx.update({'default_related_moves': str(moves_ids)})
        return {
            'name': _('Create cash statement'),
            'res_model': 'register.bank.statement',
            'view_mode': 'form',
            'context': ctx,
            'active_ids': info_carrier.id,
            'target': 'new',
            'type': 'ir.actions.act_window'
        }

    def get_statements_entries(self):
        '''Return the bank statements view with the created records.'''
        return {
            'name': _('Banks Statements Entries'),
            'view_mode': 'tree,form',
            'res_model': 'account.bank.statement',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', self.banks_statements_ids.ids)],
            'context': self._context.copy()
        }
