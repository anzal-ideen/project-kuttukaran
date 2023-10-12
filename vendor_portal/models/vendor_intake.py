from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo import modules
from odoo.http import request, _logger
import requests


class VendorIntake(models.Model):
    _name = 'vendor.intake'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # name = fields.Char(string='Number', required=True, copy=False, readonly=True,
    #                        default=lambda self: _('New'))
    name = fields.Char("Name", tracking=True)
    street = fields.Char("Street")
    address1 = fields.Char("Address 1")
    address2 = fields.Char("Address 2")
    city = fields.Char("City")
    zip = fields.Char("Pincode")
    gst = fields.Char("VAT No", tracking=True)
    pan = fields.Char("Pan No", tracking=True)
    tel = fields.Char("Telephone No", tracking=True)
    mob = fields.Char("Mobile No", tracking=True)
    mail_id = fields.Char("Email ID", tracking=True)
    state_id = fields.Char("State")
    state_ids = fields.Many2one('res.country.state', "State")
    country_id = fields.Many2one(string="Country", comodel_name='res.country', help="Country")
    # user_id = fields.Many2one('res.users', string='Contact User', default=lambda self: self.env.user,)
    ref = fields.Char("Vendor Reference")
    contactperson = fields.Char("Contact Person 1")
    contactperson2 = fields.Char("Contact Person 2")
    msme = fields.Char("MSME Category")
    remarks = fields.Text("Remarks")
    states = fields.Selection([("draft", "Draft"), ("approved", "Approved"), ("done", "User Generated"), ],
                              string="Status", default="draft", tracking=True)

    bank = fields.Char(string='Bank Name')
    bank_acc_no = fields.Char(string='Account No')
    branch = fields.Char(string="Branch")
    ifsc = fields.Char(string="IFSC Code")

    msme_number = fields.Char(string="MSME Number")
    vendor_category = fields.Many2one("product.category",string="Vendor Category")
    # company_type = fields.Char(string="Company Type")
    company_type = fields.Selection([
        ('type1', 'Companies Limited by Shares'),
        ('type2', 'Companies Limited by Guarantee'),
        ('type3', 'Unlimited Companies'),
        ('type4', 'One Person Companies (OPC)'),
        ('type5', 'Private Companies'),
        ('type6', 'Public Companies'),
        ('type7', 'Holding and Subsidiary Companies'),
        ('type8', 'Associate Companies'),
        ('type9', 'Companies in terms of Access to Capital'),
        ('type10', 'Government Companies'),
        ('type11', 'Foreign Companies'),
        ('type12', 'Charitable Companies'),
        ('type13', 'Dormant Companies'),
        ('type14', 'Nidhi Companies'),
        ('type15', 'Public Financial Institutions'),
    ], string="Company Type")
    website = fields.Char(string="Website Link")
    gst_file = fields.Binary(string='Uploaded File')
    pan_card = fields.Binary(string='Pan Card file')
    bank_file = fields.Binary(string='Statement Copy file')
    bank_cheque_file = fields.Binary(string='Bank Cheque file')

    # vendor_bank_line_ids = fields.One2many('vendor.bank.line', 'vendor_line_id', string='Vendor Bank line')

    # def action_validate(self):
    #
    #     # Replace with the GST number you want to check
    #     gst_number = "22ABCDE1234F1Z5"
    #     key_secret = "6GILxGgI7tVgy00FzTWN75v76LO2"
    #
    #     # Define the URL for the GSTIN verification API
    #     url = f" https://appyflow.in/api/verifyGST={gst_number}"
    #
    #     # Make a GET request to the API
    #     response = requests.get(url)
    #
    #     # Check if the request was successful (status code 200)
    #     if response.status_code == 200:
    #         data = response.json()
    #         if data["status_cd"] == "1":
    #             print("GST Number is valid.")
    #             print("Legal Name:", data["tradeNam"])
    #             print("State Jurisdiction:", data["stj"])
    #             print("Center Jurisdiction:", data["ctj"])
    #         else:
    #             print("GST Number is not valid.")
    #     else:
    #         print("Failed to retrieve GST details. Status code:", response.status_code)

    # self.states='validate'

    def action_approve(self):
        self.ref = self.env['ir.sequence'].next_by_code('vendor.intake')

        # vendor_exist = self.env['res.partner'].sudo().search([
        #     ('vat', '=', self.gst)])
        # if vendor_exist:
        #     raise UserError("Vendor GST is already exist")
        # else:
        #     user_generated = self.env['res.partner'].sudo().create({
        #         "name": self.name,
        #         "street": self.address1,
        #         "street2": self.street,
        #         "street2": self.street,
        #         "city": self.city,
        #         # "state_id":self.state_id.id,
        #         "zip": self.zip,
        #         # "country_id":self.country_id.id,
        #         "email": self.mail_id,
        #         "vat": self.gst,
        #         "mobile": self.mob,
        #     })
        self.states = 'approved'

    def action_done(self):
        if self.gst and self.mail_id:
            vendor_exist = self.env['res.partner'].sudo().search([
                ('vat', '=', self.gst)])
            if vendor_exist:
                raise UserError("Vendor GST is already exist")
            else:
                vendor_generated = self.env['res.partner'].sudo().create({
                    "name": self.name,
                    "street": self.address1,
                    "street2": self.street,
                    "street2": self.street,
                    "city": self.city,
                    # "state_id":self.state_id.id,
                    "zip": self.zip,
                    # "country_id":self.country_id.id,
                    "email": self.mail_id,
                    "vat": self.gst,
                    # "mobile": self.mob,
                })

            if vendor_generated:

                user_exist = self.env['res.users'].sudo().search([('name', '=', self.name),
                                                                  ('login', '=', self.mail_id)])
                if user_exist:
                    raise UserError("Login already exist")
                else:
                    password = self.ref
                    user_generated = self.env['res.users'].sudo().create({
                        'name': self.name,
                        'login': self.mail_id,
                        'password': password,
                        'partner_id': vendor_generated.id,
                        'sel_groups_1_9_10': "1",  # Assign group 1
                        'sel_groups_58_59': "58",  # Assign group 58
                        'in_group_76': True,
                    })

                    # user_generated = self.env['res.users'].sudo().create({
                    #     'name': self.name,
                    #     'login': self.mail_id,
                    #     'password': password,
                    #     'partner_id': vendor_generated.id,
                    #     # 'partner_id':
                    #     'sel_groups_1_9_10': "1",
                    #     # 'sel_groups_24_25_26': False,
                    #     # 'sel_groups_30_31_32': "false",
                    #     'sel_groups_58_59': "58",
                    #     # 'sel_groups_13_14': False,
                    #     'in_group_76': True,
                    # })
            body = (
                        "Dear Vendor,Your vendor registration has been successfully approved and your Login id is" + " " + self.mail_id + " "
                                                                                                                                          "Password is" + " " + password)
            vals = {
                'subject': 'Vendor Login Credentials',
                'body_html': body,
                'email_to': self.mail_id,
                'auto_delete': False,
                # 'email_from': ,
            }
            # print(vals)
            mail_id = self.env['mail.mail'].sudo().create(vals)
            mail_id.sudo().send()
            self.states = 'done'
        else:
            raise UserError("Please ensure GST and Mail Id are entered correctly")

    def action_draft(self):
        if self.states == "done":
            user_found = self.env['res.users'].sudo().search([('name', '=', self.name),
                                                              ('login', '=', self.mail_id)])
            if user_found:
                raise UserError("Please delete the related User & Vendor to countinue")
            else:
                self.states = 'approved'

        # elif self.states == "approved":
        #     vendor_found = self.env['res.partner'].sudo().search([
        #         ('vat', '=', self.gst)])
        #     if vendor_found:
        #         raise UserError("Please delete the related Vendor to countinue")
        #     else:
        #         self.states = 'draft'

        else:
            self.states = 'draft'

    # @api.model
    # def create(self, vals):
    #     if vals.get('name', _('New')) == _('New'):
    #         vals['name'] = self.env['ir.sequence'].next_by_code('vendor.intake') or _('New')
    #     res = super(VendorIntake, self).create(vals)
    #     return res

# class VendorBankLines(models.Model):
#     _name = "vendor.bank.line"
#
#     bank = fields.Char( string='Bank Name')
#     bank_acc_no = fields.Char(string='Account No')
#     branch = fields.Char(string="Branch")
#     ifsc = fields.Char(string="IFSC Code")
#
#     vendor_line_id = fields.Many2one('vendor.intake', string='Bank Lines')
