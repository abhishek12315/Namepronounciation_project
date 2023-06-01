# from google.oauth2.credentials import Credentials
# from googleapiclient.discovery import build
# import pandas as pd

# creds = Credentials.from_authorized_user_file('credentials.json')
# service = build('forms', 'v1', credentials=creds)

# response = service.forms().responses().list(formId='1FvJGgdUXZc6lwd3GeZ42Dy8BmLZkyQQIBrgQK2hmF5k').execute()
# df = pd.DataFrame(response['responses'])
# print(df)
from google.oauth2 import service_account
from google.auth.transport.requests import Request

def authenticate():
    credentials = service_account.Credentials.from_service_account_file('credentials.json')
    if credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())
    return credentials

from googleapiclient.discovery import build

def get_form_responses(form_id):
    service = build('forms', 'v1', credentials=authenticate())
    response = service.forms().responses().get(formId="1FvJGgdUXZc6lwd3GeZ42Dy8BmLZkyQQIBrgQK2hmF5k", fullResource=True).execute()
    return response

form_responses = get_form_responses('1FvJGgdUXZc6lwd3GeZ42Dy8BmLZkyQQIBrgQK2hmF5k')

