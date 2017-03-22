"""searcher command line tool."""
# -*- coding: utf-8 -*-
import logging
import os
import sqlite3
import sys

from datetime import datetime

from searcher.web import search_web_browsers


class Searcher:
    def __init__(self):
        self.daum_client_id = os.environ.get('DAUM_CLIENT_ID')  # daum
        self.daum_secret = os.environ.get('DAUM_CLIENT_SECRET')
        self.daum_app_key = os.environ.get('DAUM_APP_KEY')
        self.naver_client_id = os.environ.get('NAVER_CLIENT_ID')  # naver
        self.naver_secret = os.environ.get('NAVER_CLIENT_SECRET')
        self.keys = []

        now = datetime.now()  # log
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

    search_web_browsers(s)  # start
    sys.exit(0)
