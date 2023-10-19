import boto3
from io import BytesIO, StringIO
import base64
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date, datetime, time
import subprocess
import tempfile


class FileUpload(models.Model):
    _name = "file.upload"
    _description = "File Upload"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Number', required=True, copy=False, readonly=True,
                       default=lambda self: _('New'))
    description = fields.Char("Description", required=True,tracking=True)
    date = fields.Date("Date", default=date.today())
    user_id = fields.Many2one('res.users', string='Responsible', required=False, default=lambda self: self.env.user)
    file = fields.Binary(string='File Upload')
    url = fields.Char(string='URL', readonly=True)
    uploaded = fields.Boolean("Uploaded", default=False)

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('file.upload') or _('New')
        res = super(FileUpload, self).create(vals)
        return res

    def action_upload(self):
        print("hellooooooo")
        action = self.env["ir.actions.actions"]._for_xml_id('file_upload.upload_file_action')
        action['context'] = {'default_upload_id': self.id}

        return action

    # def action_amazon_upload(self):
    #     print("gggg")


class UploadWizard(models.TransientModel):
    _name = "file.upload.wizard"
    _description = "File Upload"

    file_name = fields.Char("Name")
    file = fields.Binary(string='File Upload')
    upload_id = fields.Many2one(
        'file.upload', string='Upload', readonly=True)

    def confirm_upload(self):

        access_key = self.env['ir.config_parameter'].get_param(
            'amazon_s3_connector.amazon_access_key')
        secret_key = self.env[
            'ir.config_parameter'].get_param(
            'amazon_s3_connector.amazon_secret_key')
        bucket = (self.env['ir.config_parameter'].get_param(
            'amazon_s3_connector.amazon_bucket_name'))

        key = f"{str(self.upload_id)}_{self.file_name}"

        attachment = self.env["ir.attachment"].search(
            ['|', ('res_field', '!=', False), ('res_field', '=', False),
             ('res_id', '=', self.id),
             ('res_model', '=', 'file.upload.wizard')])
        try:
            client = boto3.resource(
                's3',
                aws_access_key_id=self.env['ir.config_parameter'].get_param(
                    'amazon_s3_connector.amazon_access_key'),
                aws_secret_access_key=self.env[
                    'ir.config_parameter'].get_param(
                    'amazon_s3_connector.amazon_secret_key'))
            client.Bucket(self.env['ir.config_parameter'].get_param(
                'amazon_s3_connector.amazon_bucket_name')).put_object(
                # Key=self.file_name,
                Key=key,
                Body=open((attachment._full_path(attachment.store_fname)),
                          'rb'))

            file_url = f"https://{bucket}.s3.amazonaws.com/{key}"
            #
            #
            self.upload_id.uploaded = True
            self.upload_id.url = file_url
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
        except Exception as e:
            raise ValidationError(
                'Failed to Upload Files ( %s .)' % e)

        # local_file = self.file
        # BUCKET_NAME = bucket
        # s3_file =self.file_name
        #
        #
        #
        #
        # aws_command = f"aws s3 cp {local_file} s3://{BUCKET_NAME}/{s3_file} --acl public-read"
        #
        # try:
        #     subprocess.run(aws_command, shell=True, check=True)
        #     # print(f"Successfully uploaded {local_file} to {s3_file}")
        #     return True
        # except subprocess.CalledProcessError as e:
        #     # print(f"Failed to upload {local_file} to {s3_file}: {e}")
        #     return False
        #
        #
        # # Example usage
        # local_file_path = 'path/to/local/file.txt'  # Path to the local file you want to upload
        # s3_file_path = 's3-folder-name/remote-file.txt'  # Path and name for the file in the S3 bucket
        #
        # if upload_to_aws_s3(local_file_path, s3_file_path):
        #     print("passs")
        # # The file was uploaded successfully
        # # You can perform any additional tasks here if needed
        # else:
        #     print("fail")



        # ...

        # for record in self:
        #     if record.file:
        #         bucket_name="odoo001"
        #         file_name = record.file_name
        #         # ...
        #
        #         try:
        #             # Prepare the file for upload to S3
        #             with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        #                 temp_file_path = temp_file.name
        #                 temp_file.write(file_content)
        #
        #             # Upload the file to S3 using AWS CLI
        #             aws_s3_cp_command = f"aws s3 cp '{temp_file_path}' 's3://{bucket_name}/{file_name}'"
        #             result = subprocess.run(aws_s3_cp_command, shell=True, check=True, stderr=subprocess.PIPE)
        #
        #             if result.returncode != 0:
        #                 raise subprocess.CalledProcessError(result.returncode, aws_s3_cp_command, result.stderr)
        #
        #             # Construct the S3 URL
        #             file_url = f"https://{bucket_name}.s3.amazonaws.com/{file_name}"
        #
        #             # Cleanup: Remove the temporary file
        #             subprocess.run(f"rm {temp_file_path}", shell=True, check=True)
        #
        #             # Update your model with the S3 URL
        #             record.write({'file_url': file_url})
        #
        #             return {
        #                 'type': 'ir.actions.client',
        #                 'tag': 'display_notification',
        #                 'params': {
        #                     'type': 'success',
        #                     'message': 'File has been uploaded successfully. '
        #                                'Please refresh the page.',
        #                     'next': {'type': 'ir.actions.act_window_close'},
        #                 }
        #             }
        #         except subprocess.CalledProcessError as e:
        #             raise ValidationError(f'Failed to upload file to S3: {e}')
        #         except Exception as e:
        #             raise ValidationError(f'Error: {e}')
        #     else:
        #         raise ValidationError('No file attached to upload.')

        # for record in self:
        #     if record.file:
        #         bucket_name = bucket
        #         file_name = record.file_name
        #         file_content = record.file
        #
        #         try:
        #             # Prepare the file for upload to S3
        #             temp_file_path = '/tmp/' + file_name  # Define a temporary path for the file
        #             with open(temp_file_path, 'wb') as temp_file:
        #                 temp_file.write(file_content)
        #
        #             # Upload the file to S3 using AWS CLI
        #             aws_s3_cp_command = f"aws s3 cp {temp_file_path} s3://{bucket_name}/{file_name}"
        #             subprocess.run(aws_s3_cp_command, shell=True, check=True)
        #
        #             # Construct the S3 URL
        #             file_url = f"https://{bucket_name}.s3.amazonaws.com/{file_name}"
        #
        #             # Cleanup: Remove the temporary file
        #             subprocess.run(f"rm {temp_file_path}", shell=True, check=True)
        #
        #             # Update your model with the S3 URL
        #             record.write({'file_url': file_url})
        #
        #             return {
        #                 'type': 'ir.actions.client',
        #                 'tag': 'display_notification',
        #                 'params': {
        #                     'type': 'success',
        #                     'message': 'File has been uploaded successfully. '
        #                                'Please refresh the page.',
        #                     'next': {'type': 'ir.actions.act_window_close'},
        #                 }
        #             }
        #         except subprocess.CalledProcessError as e:
        #             raise ValidationError(f'Failed to upload file to S3: {e}')
        #
        #     else:
        #         raise ValidationError('No file attached to upload.')
        #






    ############################################################## Uploding code ###############################################



    # print("hhhhhhhh")
    #     for record in self:
    #         if record.file:
    #             access_key = self.env['ir.config_parameter'].get_param(
    #                 'amazon_s3_connector.amazon_access_key')
    #             secret_key =self.env[
    #                 'ir.config_parameter'].get_param(
    #                 'amazon_s3_connector.amazon_secret_key')
    #             bucket = (self.env['ir.config_parameter'].get_param(
    #                         'amazon_s3_connector.amazon_bucket_name'))
    #
    #             try:
    #                 s3 = boto3.client(
    #                     's3',
    #                     aws_access_key_id= access_key,
    #                     aws_secret_access_key= secret_key )
    #                 bucket_name = bucket
    #                 file_name = record.file_name
    #                 file_content = record.file
    #
    #                 # Upload the file to S3
    #                 s3.put_object(
    #                     Bucket=bucket_name,
    #                     Key=file_name,
    #                     Body=BytesIO(file_content)
    #                 )
    #                 file_url = f"https://{bucket_name}.s3.amazonaws.com/{file_name}"
    #
    #
    #                 # print(file_url)
    #                 self.upload_id.url = file_url
    #                 self.upload_id.uploaded = True
    #                 # s3.download_file(bucket_name, file_url, local_file_path)
    #
    #                 return {
    #                             'type': 'ir.actions.client',
    #                             'tag': 'display_notification',
    #                             'params': {
    #                                 'type': 'success',
    #                                 'message': 'File has been uploaded successfully. '
    #                                            'Please refresh the page.',
    #                                 'next': {'type': 'ir.actions.act_window_close'},
    #                             }
    #                         }
    #
    #                 # Optionally, you can set ACL permissions here
    #                 # s3.put_object_acl(Bucket=bucket_name, Key=file_name, ACL='public-read')
    #
    #             except Exception as e:
    #                 raise ValidationError('Failed to upload file to S3: %s' % str(e))
    #         else:
    #             raise ValidationError('No file attached to upload.')
