"""searcher command line tool."""
# -*- coding: utf-8 -*-
import httplib2
import logging
import os
import sqlite3
import sys

from apiclient import discovery
from datetime import datetime
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from twython import Twython
from searcher.web import search_webs


class Searcher:
    def __init__(self):
        self.operator_name = os.environ.get('MOHW_OPERATOR')  # daum

        self.twitter_app_key = os.environ.get('TWITTER_APP_KEY')
        self.twitter_app_secret = os.environ.get('TWITTER_APP_SECRET')
        self.twitter_access_token = os.environ.get('TWITTER_ACCESS_TOKEN')
        self.twitter_access_secret = os.environ.get('TWITTER_ACCESS_SECRET')
        self.twitter_id = os.environ.get('TWITTER_ID')
        self.twitter = Twython(
            self.twitter_app_key,
            self.twitter_app_secret,
            self.twitter_access_token,
            self.twitter_access_secret
        )

        now = datetime.now() 
        self.today = '%4d-%02d-%02d' % (now.year, now.month, now.day)

        self.daum_client_id = os.environ.get('DAUM_CLIENT_ID')  # daum
        self.daum_secret = os.environ.get('DAUM_CLIENT_SECRET')
        self.daum_app_key = os.environ.get('DAUM_APP_KEY')
        self.naver_client_id = os.environ.get('NAVER_CLIENT_ID')  # naver
        self.naver_secret = os.environ.get('NAVER_CLIENT_SECRET')
        self.keys = []

        log_file = '%s/log/searcher_%4d%02d%02d.log' % (os.getenv("HOME"),
                                                        now.year,
                                                        now.month,
                                                        now.day)
        ch = logging.StreamHandler()
        ch.setLevel(logging.ERROR)
        formatter = logging.Formatter('[%(levelname)8s] %(message)s')
        ch.setFormatter(formatter)
        logging.basicConfig(filename=log_file,
                            format='[%(asctime)s] (%(levelname)8s) %(message)s',
                            datefmt='%I:%M:%S',
                            level=logging.INFO)
        self.logger = logging.getLogger('ft_logger')
        self.logger.addHandler(ch)

        db_file_path = os.environ.get('MOHW_SQLITE3')
        self.conn = sqlite3.connect(db_file_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS sent_msg (
            "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
            "type" text,
            "info" text,
            "update_time" datetime
            )''')
        self.conn.commit()

        self.mohw_client_secret = os.environ.get('MOHW_CLIENT_SECRET')  # google sheet
        self.credential_file_name = os.environ.get('MOHW_CREDENTIAL_FILE')
        self.spreadsheetId = os.environ.get('MOHW_SPREAD_SHEET_ID')
        try:
            import argparse
            self.flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
        except ImportError:
            self.flags = None

        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?' 'version=v4')
        self.service = discovery.build('sheets', 'v4', http=http,
                                       discoveryServiceUrl=discoveryUrl)

    def get_credentials(self):
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir, self.credential_file_name)

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(self.mohw_client_secret,
                                                  'https://www.googleapis.com/auth/spreadsheets')
            flow.user_agent = 'support'  # APPLICATION_NAME
            if self.flags:
                credentials = tools.run_flow(flow, store, self.flags)
            else:  # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials

    def check_duplicate_item(self, web_info, web_type):
        if (web_type is None) or (web_info is None):
            return False
        web_info = web_info.replace('\"', '\'')  # avoid query failed
        query = 'SELECT * FROM sent_msg WHERE type="%s" and info="%s"' % (
                web_type, web_info)
        self.cursor.execute(query)
        data = self.cursor.fetchone()
        if data is None:
            return False  # not exist
        else:
            return True  # duplicated

    def match_soup_class(self, target, mode='class'):
        def do_match(tag):
            classes = tag.get(mode, [])
            return all(c in classes for c in target)
        return do_match


def main() -> None:
    s = Searcher()
    keywords = os.environ.get('MOHW_KEYWORD')  # 보건복지부
    s.keys = keywords.split(',')

    search_webs(s)  # start
    sys.exit(0)
