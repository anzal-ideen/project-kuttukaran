from odoo.http import request
from odoo import http
import base64
from odoo.addons.portal.controllers.portal import CustomerPortal

class VendorPortal(CustomerPortal):

    # @http.route(["/my/vendors"],type="http",methods=["POST","GET"], auth="public", website= True)
    @http.route(["/vendors"],type="http",methods=["POST","GET"], auth="public", website= True)

    def vendor_registration(self ,**kw):
        states_list = request.env['res.country.state'].sudo().search([])
        pdt_category = request.env['product.category'].sudo().search([])
        # gst_file_data = request.httprequest.files.get('gst_file')
        # bank_file_data = request.httprequest.files.get('bank_file')
        gst_file_data = request.httprequest.files.get('gst_file')
        bank__chequefile_data = request.httprequest.files.get('bank_cheque_file')
        pan_data = request.httprequest.files.get('pan_file')
        bank_statement = request.httprequest.files.get('bank_statement')

        print(gst_file_data)
        # print(bank_file_data)
        print(request.httprequest.files.keys())

        vals = {'vendor_states':states_list ,'pdt_category':pdt_category}

        if request.httprequest.method =="POST":
            print(kw)
            gst_file_content = base64.b64encode(gst_file_data.read()) if gst_file_data else False
            # bank_file_content = base64.b64encode(bank_file_data.read()) if bank_file_data else False
            bank_cheque_file_content = base64.b64encode(bank__chequefile_data.read()) if bank__chequefile_data else False
            pan_data_content = base64.b64encode(pan_data.read()) if pan_data else False
            bank_statement_content = base64.b64encode(bank_statement.read()) if bank_statement else False


            request.env['vendor.intake'].sudo().create(
                {
                    "name":kw.get("name"),
                    "address1":kw.get("address"),
                    "address2":kw.get("address2"),
                    "street":kw.get("street"),
                    "city":kw.get("city"),
                    "zip":kw.get("pin"),
                    # "state_id":kw.get("state"),
                    "state_ids":int(kw.get("state_id")),
                    "gst":kw.get("gst"),
                    "pan":kw.get("pan"),
                    "mob":kw.get("mobile"),
                    "mail_id":kw.get("mail"),
                    # "remarks":kw.get("remarks"),
                    "tel":kw.get("tel"),
                    "contactperson":kw.get("contactperson"),
                    "contactperson2":kw.get("contactperson2"),
                    "msme":kw.get("msme"),
                    'bank': kw.get("bank_name"),
                    'bank_acc_no': kw.get("bank_acc"),
                    'branch': kw.get("bank_branch"),
                    'ifsc':kw.get("bank_ifsc") ,
                    'msme_number':kw.get("msme_no") ,
                    'vendor_category':int(kw.get("pdt_category")) ,
                    'company_type':kw.get("type") ,
                    'website':kw.get("website") ,
                    'gst_file':gst_file_content,
                    'pan_card':pan_data_content ,
                    'bank_file':bank_statement_content ,
                    'bank_cheque_file':bank_cheque_file_content ,
                }
            )
            success = "Registration Succesfull"
            vals['success_msg'] =success
            return request.render("vendor_portal.submit_return")
            # else:
            #     vals['error_list'] =error_list
        else:
            print("GET METHOD")

        return request.render("vendor_portal.new_vendor_form_view", vals)
