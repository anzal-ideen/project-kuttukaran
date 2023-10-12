from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AsNotice(models.Model):
    _name = 'advanced.shipment.notice'

    name = fields.Char(string='Number', required=True, copy=False, readonly=True,
                           default=lambda self: _('New'))
    partner_id = fields.Many2one('res.partner', string='Partner')
    purchase_representative = fields.Many2one('res.users',"Purchase Representative")
    po_no = fields.Many2one('purchase.order',"Purchase Order")
    transfer = fields.Many2one('stock.picking',"Transfer No")
    date_approve = fields.Datetime("PO Confirmation Date")
    asn_date = fields.Datetime("Adavanced Shipment Date")
    state = fields.Selection([("draft", "Draft"), ("submit", "Submitted")], string="Status", default="draft")

    asn_line_ids = fields.One2many('asn.lines', 'asn_lines', string='ASN line')


    def action_submit(self):
        print("helloooo")
        if self.asn_date:
            self.state='submit'
            transfer = self.env['stock.picking'].search([('id', '=', self.transfer.id)])
            for tr in transfer:
                tr.asm_date = self.asn_date
        else:
            raise UserError("Please enter Advanced Shipment Date")

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('advanced.shipment.notice') or _('New')
        res = super(AsNotice, self).create(vals)
        return res


class AsnLiness(models.Model):
    _name = "asn.lines"

    product_id = fields.Many2one('product.product', string='products')
    quantity = fields.Float(string='Demand Quantity')
    provide_qty = fields.Float(string='Quantity Suppliable')
    remark = fields.Char(string="Remark")


    asn_lines = fields.Many2one('advanced.shipment.notice', string='Params')






