import boto3
from io import BytesIO, StringIO
import base64
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class FileUpload(models.Model):
    _name = "file.upload"
    _description = "File Upload"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    file_name = fields.Char("Name")
    description = fields.Char("Description")
    file = fields.Binary(string='File Upload')

    def action_upload(self):
        print("hellooooooo")

    def action_amazon_upload(self):
        for record in self:
            if record.file:
                access_key = self.env['ir.config_parameter'].get_param(
                    'amazon_s3_connector.amazon_access_key')
                secret_key =self.env[
                    'ir.config_parameter'].get_param(
                    'amazon_s3_connector.amazon_secret_key')
                bucket = (self.env['ir.config_parameter'].get_param(
                            'amazon_s3_connector.amazon_bucket_name'))

                try:
                    s3 = boto3.client(
                        's3',
                        aws_access_key_id= access_key,
                        aws_secret_access_key= secret_key )
                    bucket_name = bucket
                    file_name = record.file_name
                    file_content = record.file

                    # Upload the file to S3
                    s3.put_object(
                        Bucket=bucket_name,
                        Key=file_name,
                        Body=BytesIO(file_content)
                    )
                    file_url = f"https://{bucket_name}.s3.amazonaws.com/{file_name}"


                    print(file_url)

                    return {
                                'type': 'ir.actions.client',
                                'tag': 'display_notification',
                                'params': {
                                    'type': 'success',
                                    'message': 'File has been uploaded successfully. '
                                               'Please refresh the page.',
                                    'next': {'type': 'ir.actions.act_window_close'},
                                }
                            }

                    # Optionally, you can set ACL permissions here
                    # s3.put_object_acl(Bucket=bucket_name, Key=file_name, ACL='public-read')

                except Exception as e:
                    raise ValidationError('Failed to upload file to S3: %s' % str(e))
            else:
                raise ValidationError('No file attached to upload.')

