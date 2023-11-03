from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError

from odoo.http import request
from odoo import http
from datetime import datetime, date


class ProjectTaskInherit(models.Model):
    _inherit = "project.task"

    @api.onchange('child_ids')
    def onchange_in_child_ids(self):
        print("child_ids")
        if self.parent_id.date_deadline:
            self.date_deadline = self.parent_id.date_deadline
