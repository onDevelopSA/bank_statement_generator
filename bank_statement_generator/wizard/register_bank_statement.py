from odoo import models, fields, api, _
from odoo.exceptions import UserError
import datetime
from odoo.exceptions import ValidationError


class RegisterBankStatement(models.TransientModel):

    _name = 'register.bank.statement'

    # In this field related_moves is unnecessary use any kind of
    # relationship many .. this model is only the carrier.
    related_moves = fields.Char()
    statement_name = fields.Char(required=True)
    bank_journal = fields.Many2one('account.journal',
                                   domain=[('type', '=', 'bank')])

    def create_bank_statement(self):
        '''Generate the bank statements using the given moves.'''
        moves_ids = []
        if eval(self.related_moves):
            moves_ids = eval(self.related_moves)
        bank_statements_ids = []
        AccountMove = self.env['account.move']
        for move_id in moves_ids:
            move = AccountMove.search([('id', '=', move_id)])
            if move:
                statement_vals = {
                    'name': self.statement_name,
                    'cashbox_start_id': False,
                    'cashbox_end_id': False,
                    'journal_id': self.bank_journal.id,
                    'date': str(datetime.date.today()),
                    'line_ids': [],
                    'origin_move_id': move.id,
                    'message_follower_ids': [],
                    'message_ids': []}
                for pay_move_line in move.get_payments_moves_lines():
                    amount = 0
                    if move.move_type == 'out_invoice':
                        amount = pay_move_line.credit
                    elif move.move_type == 'in_invoice':
                        amount = (-1 * pay_move_line.debit)
                    statement_vals['line_ids'].append(
                        [0, 0, {
                            'origin_payment_move_line_id': pay_move_line.id,
                            'currency_id': pay_move_line.currency_id.id,
                            'partner_bank_id': False,
                            'sequence': 1,
                            'date': str(datetime.date.today()),
                            'payment_ref': pay_move_line.ref,
                            'partner_id': pay_move_line.partner_id.id,
                            'ref': pay_move_line.ref,
                            'transaction_type': False,
                            'narration': False,
                            'amount': amount,
                            'account_number': False}])
                if len(statement_vals['line_ids']) == 0:
                    msg_error = "The invoice  {move} don't have any payment"+\
                                " to conciliate with the bank or already was"+\
                                " conciliate."
                    raise ValidationError(_(msg_error.format(move=move.name)))
                statement = self.env['account.bank.statement'].create(
                    statement_vals)
                bank_statements_ids.append(statement.id)
        action = {
            'name': _('Bank Statement'),
            'res_model': 'account.bank.statement',
            'type': 'ir.actions.act_window',
        }
        if len(bank_statements_ids) == 1:
            action.update({
                'view_mode': 'form',
                'res_id': bank_statements_ids[0],
            })
        else:
            action.update({
                'domain': [('id', 'in', bank_statements_ids)],
                'view_mode': 'tree,form'
            })
        return action
