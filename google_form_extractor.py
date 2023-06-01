from google.oauth2 import service_account
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.cloud import storage


class GoogleFormExtractor:
    def __init__(self, credentials_path):
        self.credentials_path = credentials_path

    def authenticate(self):
        credentials = service_account.Credentials.from_service_account_file(self.credentials_path)
        if credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        return credentials

    def get_form_responses(self, form_id):
        service = build('forms', 'v1', credentials=self.authenticate())
        response = service.forms().responses().list(formId=form_id).execute()
        return response

    def store_responses_in_gcs(self, bucket_name, folder_name, file_name, responses):
        storage_client = storage.Client.from_service_account_json(self.credentials_path)
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(f'{folder_name}/{file_name}')
        blob.upload_from_string(str(responses))

#%%

