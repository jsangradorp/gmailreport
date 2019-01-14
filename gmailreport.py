from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# File copied mercilessly from
# https://developers.google.com/calendar/quickstart/python
#
# Need:
#
# pip install --upgrade google-api-python-client oauth2client

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        # If needed, the credentials.json file needs to be obtained
        # in https://console.developers.google.com/apis/credentials?project=gmailreports-1547134468896&authuser=0
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('gmail', 'v1', http=creds.authorize(Http()))

    # Call the Gmail API
    results = service.users().messages().list(userId='me', labelIds=["SENT"], q="after:2019/1/14 before:2019/1/15").execute()
    labels = results.get('messages', [])

    # if not labels:
    #     print('No labels found.')
    # else:
        # print('Labels:')
    for label in labels:
        message = service.users().messages().get(userId="me", id=label['id']).execute()
        print("Sent", filter(lambda x: x['name'] == 'Subject', message['payload']['headers'])[0]['value'], "to", filter(lambda x: x['name'] == 'To', message['payload']['headers'])[0]['value'])

if __name__ == '__main__':
    main()
