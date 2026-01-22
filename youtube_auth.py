import os
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

# The CLIENT_SECRETS_FILE file specifies the client ID and client secret of the
# property or application that is making the request.
CLIENT_SECRETS_FILE = "client_secrets.json"

# This scope allows for full YouTube Management, including uploading videos.
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

def get_authenticated_service():
    if not os.path.exists(CLIENT_SECRETS_FILE):
        print(f"Error: {CLIENT_SECRETS_FILE} not found. Please download it from Google Cloud Console.")
        return None

    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_local_server(port=0)
    
    print("\n--- AUTHENTICATION SUCCESSFUL ---")
    print(f"Refresh Token: {credentials.refresh_token}")
    print(f"Client ID: {credentials.client_id}")
    print(f"Client Secret: {credentials.client_secret}")
    print("\nIMPORTANT: Copy the Refresh Token and add it to your automated_intelligence_pipeline.py script.")
    
    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

if __name__ == '__main__':
    get_authenticated_service()
