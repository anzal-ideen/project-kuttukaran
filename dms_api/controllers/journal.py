from odoo import http
from odoo.exceptions import ValidationError, UserError
from odoo.http import request, _logger
from datetime import datetime
from odoo import api, models, fields, _


class PaymentJournal(http.Controller):
    @http.route('/web/session/authenticate', type='json', auth="none")
    def authenticate(self, db, login, password, base_location=None):
        request.session.authenticate(db, login, password)
        return request.env['ir.http'].session_info()


class PaymentsJournalEntry(http.Controller):
    @http.route('/dms/payment/journal', type='json', csrf=False, auth='public')
    def create_customer_payments(self, **rec):
        # paymnt_number = []
        journal_number = []
        for record in rec["payment"]:
            reference = record["expense_reference"]
            ref = reference and request.env['account.move'].sudo().search(
                [('ref', '=', reference), ('move_type', '=', 'entry')], limit=1) or False
            if ref:
                journal_number.append({
                    'Expense_ref': record["expense_reference"],
                    'ExpenseEntryNumber': ref.id,
                    # 'payment_details.partner_type': Journal_entry.partner_type
                })
            else:
                company_id = request.env['res.company'].sudo().search(
                    [('name', '=', 'Eastea Chai Private Limited (KL)')], limit=1) or False

                reference = record["expense_reference"]

                account_date = record['date']
                if account_date:
                    date = datetime.strptime(account_date, '%d/%m/%Y')
                claim_fr_date = record['claim_from_date']
                if claim_fr_date:
                    claim_from_date = datetime.strptime(claim_fr_date, '%d/%m/%Y')
                claim_date = record['claim_to_date']
                if claim_date:
                    claim_to_date = datetime.strptime(claim_date, '%d/%m/%Y')

                code = record["analytical_code"]
                if code:
                    analytical_id = request.env['account.analytic.account'].sudo().search(
                        [('code', 'like', code), ('company_id', '=', company_id.id)], limit=1) or False
                    if not analytical_id:
                        analytical_details = {
                            'name': code,
                            'code': code,
                            'company_id': company_id.id,
                        }
                        analytical_id = request.env['account.analytic.account'].sudo().create(
                            analytical_details)
                        request.env.cr.commit()
                    analytical_id = request.env['account.analytic.account'].sudo().search(
                        [('code', 'like', code), ('company_id', '=', company_id.id)], limit=1) or False

                    employee_designation = record["emp_desig"]
                    if employee_designation:
                        # if employee_designation == "Merchandising officer" or "Sales Promoter":
                        if employee_designation in ["Merchandising officer", "Sales Promoter"]:
                            cr_acc_id = request.env['account.account'].sudo().search(
                                [('name', 'like', "Travel Expense Payable Marketing"), ('company_id', '=', company_id.id)],
                                limit=1) or False

                        else:
                            cr_acc_id = request.env['account.account'].sudo().search(
                                [('name', 'like', "Travel Expense Payable Sales"), ('company_id', '=', company_id.id)],
                                limit=1) or False

                    if not cr_acc_id:
                        journal_number.append({
                            'Expense_ref': record["expense_reference"],
                            'message': "Error, Credit Account Not Found in" +" "+ company_id.name
                        })

                    else:
                        dbt_acc_id = request.env['account.account'].sudo().search(
                            [('name', '=', 'Food, Stay & Travel Charges'), ('company_id', '=', company_id.id)], limit=1) or False

                        journalname = "Distributor Expense"
                        journal_id = journalname and request.env['account.journal'].sudo().search(
                            [('name', '=', journalname), ('company_id', '=', company_id.id)], limit=1) or False

                        amount = record["amount"]
                        Journal_entry = request.env['account.move'].sudo().create({
                            'move_type': "entry",
                            'ref': reference,
                            # 'date': date,
                            'journal_id': journal_id.id,
                            'claim_from_date': claim_from_date,
                            'claim_to_date': claim_to_date,
                            'company_id': company_id.id,
                            'line_ids': [(0, 0, {
                                'name': record["emp_desig"],
                                'debit': int(amount),
                                'account_id': dbt_acc_id.id,
                                # 'partner_id': partner_id.id,
                                'analytic_account_id': analytical_id.id
                            }), (0, 0, {
                                'name': record["emp_desig"],
                                'credit': int(amount),
                                'account_id': cr_acc_id.id,
                                # 'partner_id': partner_id.id,
                                # 'analytic_account_id': analytical_id.id
                            })]

                        })

                        if Journal_entry:
                            journal_number.append({
                                'Expense_ref': record["expense_reference"],
                                'ExpenseEntryNumber': Journal_entry.id,
                                # 'payment_details.partner_type': Journal_entry.partner_type
                            })


        return journal_number


