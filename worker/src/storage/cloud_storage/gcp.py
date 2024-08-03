from google.cloud import storage
from google.oauth2 import service_account
import os


class GCPStorage:
    def __init__(self, config):
        self.config = config
        credentials = service_account.Credentials.from_service_account_file(
            self.config.gcp_credentials_path
        )
        self.client = storage.Client(credentials=credentials)
        self.bucket = self.client.bucket(self.config.gcp_bucket_name)

    def upload_video(self, video_path, task_id):
        blob_name = f"videos/{task_id}.mp4"
        blob = self.bucket.blob(blob_name)
        blob.upload_from_filename(video_path)
        return blob.public_url

    def upload_script(self, script, task_id):
        blob_name = f"scripts/{task_id}.py"
        blob = self.bucket.blob(blob_name)
        blob.upload_from_string(script)
        return blob.public_url

    def download_video(self, task_id, destination_path):
        blob_name = f"videos/{task_id}.mp4"
        blob = self.bucket.blob(blob_name)
        blob.download_to_filename(destination_path)

    def download_script(self, task_id):
        blob_name = f"scripts/{task_id}.py"
        blob = self.bucket.blob(blob_name)
        return blob.download_as_text()

    def delete_video(self, task_id):
        blob_name = f"videos/{task_id}.mp4"
        blob = self.bucket.blob(blob_name)
        blob.delete()

    def delete_script(self, task_id):
        blob_name = f"scripts/{task_id}.py"
        blob = self.bucket.blob(blob_name)
        blob.delete()
