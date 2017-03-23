#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import httplib2

import os
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
MOHW_CLIENT_SECRET = os.environ.get('MOHW_CLIENT_SECRET')
APPLICATION_NAME = 'support'


def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_file_name = os.environ.get('MOHW_CREDENTIAL_FILE')
    credential_path = os.path.join(credential_dir, credential_file_name)

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(MOHW_CLIENT_SECRET, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def main():

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    # https://developers.google.com/sheets/guides/concepts
    spreadsheetId = os.environ.get('MOHW_SPREAD_SHEET_ID')
    print('[INFO]get value start')

#    rangeName = 'A4:A'
#    values = {'values':[['Hello Saturn',],]}
#    values = {'values': [['2', '', 'ak홍길동', '', '2016-07-06', '2016-07-06', 'http://cafe.daum.net/3664175/3vE/1029', '', '네이버', '카페', '1'],]}
    """
    searched = (['4', '', 'sssak홍길동', '', '2016-07-06', '2016-07-06', 'http://cafe.daum.net/3664175/3vE/1029', '', '네이버', '카페', '1'],
    ['5', '', 'avbak홍길동', '', '2016-07-06', '2016-07-06', 'http://cafe.daum.net/3664175/3vE/1029', '', '네이버', '카페', '1'],
    ['6', '', 'ss', '', '2016-07-06', '2016-07-06', 'http://cafe.daum.net/3664175/3vE/1029', '', '네이버', '카페', '1'],
    ['7', '', 's21231', '', '2016-07-06', '2016-07-06', 'http://cafe.daum.net/3664175/3vE/1029', '', '네이버', '카페', '1'])
    """
#    values = {'values': [searched, ]}
#    service.spreadsheets().values().append(
#        spreadsheetId=spreadsheetId, range=rangeName,
#        valueInputOption='RAW', body=values).execute()
#
    rangeName = 'Sheet1!A3:L'
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])
    if not values:
        print('No data found.')
    else:
        for row in values:
            print(row[0])
    return

if __name__ == '__main__':
    main()
