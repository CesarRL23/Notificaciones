import os
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from config import Config

class GmailService:
    @staticmethod
    def authenticate_gmail():
        creds = None
        if os.path.exists(Config.TOKEN_PATH):
            with open(Config.TOKEN_PATH, 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    Config.CREDENTIALS_PATH, Config.SCOPES)
                creds = flow.run_local_server(port=0)
            with open(Config.TOKEN_PATH, 'wb') as token:
                pickle.dump(creds, token)
        return creds

    @staticmethod
    def get_service():
        creds = GmailService.authenticate_gmail()
        return build('gmail', 'v1', credentials=creds)

    @staticmethod
    def send_message(service, user_id, message):
        try:
            sent_message = service.users().messages().send(
                userId=user_id, body=message).execute()
            return {"success": True, "message_id": sent_message['id']}
        except Exception as e:
            return {"success": False, "error": str(e)}