from odoo import fields, models
import base64
import logging
import xlrd
from datetime import datetime
from odoo.exceptions import ValidationError


class Project(models.Model):
    _inherit = 'project.project'
    _description = 'Project'

    file_upload = fields.Binary(
        string='File Upload',
        attachment=True,
    )

    def _map_fields(self, column_name):
        # print("_map_fields")
        """Map Excel column headers to Odoo fields."""
        field_map = {
            "project_id": "project_id",
            "task_name": "task_name",
            "assignees": "assignees",
            "deadline": "deadline"
        }
        return field_map.get(column_name, "")

    def excel_upload(self):
        # try:
        data = {}
        file_content = base64.b64decode(self.file_upload)
        workbook = xlrd.open_workbook(file_contents=file_content)
        worksheet = workbook.sheet_by_index(0)
        for i in range(1, worksheet.nrows):
            for j in range(worksheet.ncols):
                column_name = worksheet.cell(0, j).value
                field_name = self._map_fields(column_name)
                # Get the cell value and add to the data dictionary
                if field_name:
                    cell_value = worksheet.cell(i, j).value
                    if field_name == 'project_id' and cell_value:
                        if self.id != int(cell_value):
                            raise ValidationError("Invalid Project Id!")
                        data[field_name] = cell_value
                    elif field_name == 'deadline':
                        if not cell_value:
                            raise ValidationError("Task deadline date is missing!")
                        date_tuple = xlrd.xldate_as_tuple(cell_value, workbook.datemode)
                        date = datetime(*date_tuple).date()
                        data[field_name] = date
                    elif field_name == 'assignees' and cell_value:
                        try:
                            if ',' in cell_value:
                                user_id_list = [int(user_id) for user_id in cell_value.split(',') if
                                                user_id]
                                data[field_name] = user_id_list
                            else:
                                data[field_name] = int(cell_value)
                        except Exception as e:
                            raise ValidationError("Invalid data found in Excel employee field row: " + str(i))
                    elif field_name == 'task_name' and cell_value:
                        data[field_name] = cell_value
                    else:
                        raise ValidationError("Invalid field name. Field names should be project_id, task_name, "
                                              "assignees, deadline")
            for user_id in data['assignees']:
                records = self.env['res.users'].search([('id', '=', user_id)])
                if not records:
                    raise ValidationError("Invalid User id: " + user_id)
            values = {
                'project_id': int(data['project_id']),
                'name': data['task_name'],
                'user_ids': data['assignees'],
                'date_deadline': data['deadline']
            }
            new_record = self.env['project.task'].sudo().create(values)
        msg = "Success"
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'message': msg,
                'type': 'success',
                'sticky': True,
                'next': {
                    'type': 'ir.actions.act_window_close',
                }
            }
        }

