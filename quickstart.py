from __future__ import print_function

import os.path
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

config = json.loads(open("tempConfig.json").read())
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']


def main():

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        # sheet = service.spreadsheets()
        # The spreadsheet to request.
        spreadsheet_id = config["anon"]  # TODO: Update 
        # The A1 notation of the values to retrieve.
        range_ = 'A:Z'  # TODO: Update placeholder value.

        # How values should be represented in the output.
        # The default render option is ValueRenderOption.FORMATTED_VALUE.
        value_render_option = 'FORMATTED_VALUE'  # TODO: Update placeholder value.

        # How dates, times, and durations should be represented in the output.
        # This is ignored if value_render_option is
        # FORMATTED_VALUE.
        # The default dateTime render option is [DateTimeRenderOption.SERIAL_NUMBER].
        date_time_render_option = 'FORMATTED_STRING'  # TODO: Update placeholder value.
        
        request = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_, valueRenderOption=value_render_option, dateTimeRenderOption=date_time_render_option)
        response = request.execute()

        print(response);
    except HttpError as err:
        print(err)


if __name__ == '__main__':
    main()