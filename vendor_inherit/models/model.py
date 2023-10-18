from odoo import api, fields, models, _


class PartnerInheritFields(models.Model):
    _inherit = 'res.partner'

    new_code = fields.Char(string="Vendor Code")



    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        if not args:
            args = []
        domain = ['|', ('new_code', operator, name), ('name', operator, name)]
        records = self.search(domain + args, limit=limit)
        return records.name_get()