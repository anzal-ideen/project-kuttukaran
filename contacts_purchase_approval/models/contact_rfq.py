from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo import modules
from odoo.http import request, _logger







class PurchaseOrderAttachments(models.Model):
    _inherit = 'purchase.order'

    request_id = fields.Many2one("approval.request","Approval Request")
    attachment_number = fields.Char("number")



    def action_view_attachments(self):
        print("jjjjjj")
        # return{
        #         'type': 'ir.actions.act_window',
        #         'name': 'Attachments',
        #         'view_mode': 'tree,form',
        #         'res_model': 'ir.attachment',
        #         'domain':[('res_model','=','approval.request'), ('res_id', 'in', self.request_id.ids)] ,
        #         'target':'current'
        #     }
    
        res = self.env['ir.actions.act_window']._for_xml_id('base.action_attachment')
        res['domain'] = [('res_model', '=', 'approval.request'), ('res_id', 'in', self.request_id.ids)]
        res['context'] = {'default_res_model': 'approval.request', 'default_res_id': self.request_id.ids}
        return res

     



class RfqApprovals(models.Model):
    _inherit = 'approval.request'



    reference = fields.Char(string='Reference')


    

    @api.constrains('partner_id')
    def _check_partner_id(self):
        if self.category_id.approval_type == 'purchase':
            if not self.partner_id:
                raise UserError(_('Please add contacts field'))
            else:
                pass
        else:
            pass



    # def action_create_purchase_orders(self):
    #     po_vals = super(RfqApprovals, self).action_create_purchase_orders()
    #     if self.partner_id:
    #         po_vals['partner_id'] = self.partner_id.id
    #     return po_vals
    
class ApprovalProductLineInherited(models.Model):
    _inherit = 'approval.product.line'


    unit_price = fields.Float("Unit Price")

    def _get_purchase_order_values(self, vendor):
        vals = super()._get_purchase_order_values(vendor)
        if self.approval_request_id.partner_id:
            vals['partner_id'] = self.approval_request_id.partner_id.id
            vals['request_id'] = self.approval_request_id.id
            vals['partner_ref'] = self.approval_request_id.reference

        return vals
    
       
        # approval_request = self.approval_request_id.id
        # approval_id = self.env['approval.request'].search(
        #             [('id', '=',approval_request), ('company_id', '=', self.warehouse_id.id)])
        # if approval_id.partner_id:
        #     vals['partner_id'] = approval_id.partner_id.id
        # return vals

    def _prepare_purchase_order_line(self,po_line_vals):
        res = super()._prepare_purchase_order_line(po_line_vals)
        res.update({'price_unit': self.unit_price})
        return res
    




    

    def _check_products_vendor(self):
        # if self.approval_request_id.partner_id:
        pass
        # else:
        #     res = super(RfqApprovals, self)._check_products_vendor()
        #     return res

   
    


    






