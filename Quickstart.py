# Initial setup for allowing authorization is here:
#     https://developers.google.com/sheets/api/quickstart/python
#
# If you already have your authorization files, remember to run this:
#     pip install --upgrade google-api-python-client
#                           google-auth-httplib2
#                           google-auth-oauthlib

from __future__ import print_function
import datetime
import random
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
# Note: This scope is read/write. See other scopes here:
#     https://developers.google.com/sheets/api/guides/authorizing
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
# These must be changed for your application
SPREADSHEET_ID    = '1WS0uvF-a3Ui33ejOuZlW0wTZSjfSaXbqg3Hq_xjRuSM'
SPREADSHEET_RANGE = "Python!A:B"

def confirm_credentials( my_creds ):
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            my_creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not my_creds or not my_creds.valid:
        if my_creds and my_creds.expired and my_creds.refresh_token:
            my_creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            my_creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return my_creds

def main():
    creds = None # default to no credentials, let them be loaded
    creds = confirm_credentials( creds )
    # Get the sercice connection
    service = build('sheets', 'v4', credentials=creds)
    # Infinite loop to continuously run, as application will in the future.
    # There is a break condition for "quit".
    while ( True ):
        in       = input( "Awaiting Input\n") # Holds until Input is entered
        time_now = datetime.datetime.now( )   # Grab time for timestamp

        if ( in.lower( )=="quit" ):
            break
        # Builds up the resource that's going to be uploaded
        resource = {
            "majorDimension": "ROWS",          # Each main box will be one of these
            "values": [[in, str( time_now )]], # One row, two values
        }
        # Prepare a request
        request = service.spreadsheets( ).values( ).append(
            spreadsheetId=SPREADSHEET_ID,
            range=SPREADSHEET_RANGE,
            body=resource,
            valueInputOption="RAW", )
        # Get the response from the execution. This isn't handled, but assumed successful.
        response = request.execute( )
        print( "Uploaded!" )

if __name__ == '__main__':
    main()
