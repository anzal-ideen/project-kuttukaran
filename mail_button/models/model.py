from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo import modules
from odoo.http import request, _logger
import requests


class SaleInheritMail(models.Model):
    _inherit = 'sale.order'

    def mail_button(self):
        print("hellllllll")

        body = (
            "Hi, Mail Button test"
            "<p>"
            "<a href='http://13.51.177.228:8069/'"
            " style='background-color: #008CBA; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;'>Approve</a>"
            "<a href='http://localhost:8021/web#id=32&menu_id=321&action=472&model=tender.request&view_type=form'"
            " style='background-color: #ff0000; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;'>Reject</a>"
            "</p>"
        )

        vals = {
            'subject': 'Mail Button Test',
            'body_html': body,
            'email_to': self.partner_id.email,
            'auto_delete': False,
        }

        mail_id = self.env['mail.mail'].sudo().create(vals)
        mail_id.sudo().send()
