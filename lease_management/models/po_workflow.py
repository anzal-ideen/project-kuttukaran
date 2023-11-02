from datetime import datetime
from datetime import date
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, MissingError, UserError


class PurchaseApprovals(models.Model):
    _inherit = "purchase.order"



    approvers_line_ids = fields.One2many('po.approve.line',
                                         'po_approve_id',
                                         string='Purchase Approve Line',
                                         tracking=True)
    is_confirmed = fields.Boolean("Is Confirmed")
    is_an_approver = fields.Boolean("Approver",compute='compute_is_an_approver')


    approve_users = fields.Many2many(
        'res.users',
        'rel_po_apprvers',
        'po_id',
        'po_user',
        string='Approve Users',
    )
    approved_users = fields.Many2many(
        'res.users',
        'approved_po_relation',
        'po_apprved',
        'po_user_id',
        string='Approved Users',
    )

    next_approve_user = fields.Many2many(
        'res.users',
        'next_aprved_po',
        'next_po',
        'po_users_id',
        string='Next Approver', )

    @api.depends('next_approve_user')
    def compute_is_an_approver(self):
        for rec in self:
            rec.is_an_approver = self.env.user.id in rec.next_approve_user.mapped('id')

    def button_confirm(self):
        print("helllooo worldddd")
        if self.is_confirmed != True:
            pr_company_data = self.env['pr.company'].sudo().search([
                ('company_id', '=', self.company_id.id),
                ('location', '=', self.location.id),
                ('department_id', '=',self.department_id.id),
                ('from_amount', '<=', self.amount_total),
                ('to_amount', '>=', self.amount_total),
                ('type','=','purchase')],
               limit=1)
            print(pr_company_data)
            if pr_company_data:
                # self.message_post(body="Wait for PO"+" "+ self.name+" " +"Approval")
                self.message_post(body="Wait for Vendor acknowledgement")
                if self.partner_id.user_id:
                    new_line_vals = {
                        'user_id': self.partner_id.user_id.id,
                        'approve_order': int(1),
                    }
                    self.approvers_line_ids |= self.env['po.approve.line'].create(new_line_vals)

                for approvers in pr_company_data.pr_approve_users_id:
                    line = []
                    last_approve_order = None
                    print(approvers)
                    for users in approvers:
                        self.write({'approve_users': [(4, users.user_id.id)]})
                        if self.partner_id.user_id:
                            approve_order = int(users.approve_order) + 1
                        else:
                            approve_order = users.approve_order
                        vals = {
                            'user_id': users.user_id.id,
                            'company_id': users.company_id.id,
                            'location': users.location.id,
                            'department_id': pr_company_data.department_id.id,
                            'designation': users.designation.id,
                            'approve_order': approve_order,
                        }
                        line.append((0, 0, vals))
                        if last_approve_order is None or users.approve_order > last_approve_order:
                            last_approve_order = users.approve_order
                        print(last_approve_order)
                    self.approvers_line_ids = line
                next_approver_user_ids = [next_approver.user_id.id for next_approver in self.approvers_line_ids if
                                          next_approver.approve_order == 1]
                print(next_approver_user_ids, "This print")
                if all(item is not False for item in next_approver_user_ids):
                    self.write({'next_approve_user': [(6, 0, next_approver_user_ids)]})
                    self.is_confirmed = True
                else:
                    res = super(PurchaseApprovals, self).button_confirm()
            else:
                # raise UserError("Please make sure all the approvers approved or not")
                res = super(PurchaseApprovals, self).button_confirm()
                return res
        else:
            res = super(PurchaseApprovals, self).button_confirm()
            return res

    def action_approval(self):
        self.message_post(body=self.env.user.name +" "+"Approved")
        print("approvee")
        print("Hellooo users")
        print(self.env.user.id)
        self.write({'approved_users': [(4, self.env.user.id)]})
        self.is_an_approver = False
        self.write({'next_approve_user': [(3, self.env.user.id)]})
        approver = self.env['po.approve.line'].sudo().search(
            [('po_approve_id', '=', self.id), ('user_id', '=', self.env.user.id)])
        for record in approver:
            record.write({'status': 'approve'})

        approve_users = self.env['po.approve.line'].sudo().search(
            [('po_approve_id', '=', self.id)], order='approve_order asc')

        user_ids = [{'u_id': user.user_id.id, 'order': user.approve_order} for user in approve_users]
        # user_ids = [{'u_id': user.user_id.id, 'order': user.approve_order} for user in approve_users]
        current_order = None
        next_user = None

        for user in user_ids:
            if self.env.user.id == user['u_id']:
                current_order = user['order']

        if current_order is not None:
            for user in user_ids:
                if user['order'] == current_order + 1:
                    next_user = user

        if next_user:
            next_user_id = next_user['u_id']
            next_order = next_user['order']
            self.write({'next_approve_user': [(4, next_user_id)]})

            print("Next User ID:", next_user_id)
            print("Next Order:", next_order)
        else:
            all_approved = all(approver.status == 'approve' for approver in approve_users)

            if all_approved:
                self.is_confirmed = True
                self.button_confirm()
                # self.state = 'approve'
                print("approved")
                # Change the state to the desired value when all statuses are 'approve'
                # self.write({'state': 'approved_state'})
            else:
                # Handle the case when not all statuses are 'approve'
                # self.write({'state': 'pending_state'})
                print("not approved")

            # self.state = 'approve'
            print("Current user is the last approver or not found.")

    def action_rejected(self):
        print("rejectttt")
        self.message_post(body=self.env.user.name + " " + "Rejected")
        self.write({
            'state': 'cancel',
            'is_confirmed': False,
            'approvers_line_ids': [(5, 0, 0)],
            'approve_users': [(5, 0, 0)],
            'approved_users': [(5, 0, 0)],
            'next_approve_user': [(5, 0, 0)],
        })

    def button_cancel(self):
        res = super(PurchaseApprovals, self).button_cancel()
        self.write({
            'state': 'cancel',
            'is_confirmed': False,
            'approvers_line_ids': [(5, 0, 0)],
            'approve_users': [(5, 0, 0)],
            'approved_users': [(5, 0, 0)],
            'next_approve_user': [(5, 0, 0)],
        })

        return res


class PoApproveLines(models.Model):
    _name = "po.approve.line"
    _description = "PO Approvers Lines"

    po_approve_id = fields.Many2one('purchase.order', string='PO Approve',
                                    invisible=True)

    user_id = fields.Many2one('res.users', string="User")
    company_id = fields.Many2one('res.company', string="Company")
    location = fields.Many2one('res.company', string="Location")
    department_id = fields.Many2one('hr.department', string="Department")
    emp_name = fields.Many2one('hr.employee', string="Employee")
    designation = fields.Many2one('hr.job', string="Designation")
    approve_order = fields.Integer(string="Order")
    status = fields.Selection(
        selection=[('draft', 'Draft'), ('approve', 'Approved'), ('cancel', 'Cancel'), ('deligate', 'Deligated')],
        string='Status',
        default='draft',
        required=True, tracking=True
    )
