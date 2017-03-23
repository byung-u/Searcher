#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os
import urllib.request
import re
import sys

from bs4 import BeautifulSoup
from requests import get

from find_the_treasure.ft_sqlite3 import UseSqlite3


class FTbot:  # Find the Treasure
    def __init__(self):

        self.twitter_app_key = os.environ.get('TWITTER_APP_KEY')
        self.twitter_app_secret = os.environ.get('TWITTER_APP_SECRET')
        self.twitter_access_token = os.environ.get('TWITTER_ACCESS_TOKEN')
        self.twitter_access_secret = os.environ.get('TWITTER_ACCESS_SECRET')
        self.twitter_id = os.environ.get('TWITTER_ID')

        self.github_id = os.environ.get('GITHUB_ID')
        self.github_p = os.environ.get('GITHUB_PW')
        self.github_client_id = os.environ.get('GITHUB_CLIENT_ID')
        self.github_client_secret = os.environ.get('GITHUB_CLIENT_SECRET')

        self.naver_client_id = os.environ.get('NAVER_CLIENT_ID')
        self.naver_secret = os.environ.get('NAVER_CLIENT_SECRET')

        self.daum_client_id = os.environ.get('DAUM_CLIENT_ID')
        self.daum_secret = os.environ.get('DAUM_CLIENT_SECRET')
        self.daum_app_key = os.environ.get('DAUM_APP_KEY')

        self.google_id = os.environ.get('GOOGOLE_ID')
        self.google_p = os.environ.get('GOOGOLE_PW')
        self.gmail_from_addr = os.environ.get('GOOGOLE_FROM_ADDR')
        self.gmail_to_addr = os.environ.get('GOOGOLE_TO_ADDR')

        self.apt_trade_url = os.environ.get('DATA_APT_TRADE_URL')
        self.apt_trade_svc_key = os.environ.get('DATA_APT_API_KEY')
        self.apt_trade_dong = os.environ.get('REALESTATE_DONG')
        self.apt_trade_district_code = os.environ.get('REALESTATE_DISTRICT_CODE')
        # self.apt_trade_apt = os.environ.get('DATA_GO_KR', 'apt', raw=True)
        # self.apt_trade_size = os.environ.get('DATA_GO_KR', 'size', raw=True)

        self.rate_of_process_key = os.environ.get('RATE_OF_PROCESS_KEY')
        self.area_dcd = os.environ.get('ROP_AREA_DCD')
        self.keyword = os.environ.get('ROP_KEYWORD')

    def match_soup_class(self, target, mode='class'):
        def do_match(tag):
            classes = tag.get(mode, [])
            return all(c in classes for c in target)
        return do_match


class UseDaum:
    def __init__(self, ft):
        self.sqlite3 = UseSqlite3('daum')

    def read_other_blog_link(self, ft, url):

        r = get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        #print(soup)
        #for a in soup('meta'):
        #for a in soup.find_all(attrs={'name':'description'})
        for a in soup.find_all('meta', property="ks:richscrap"):
            res = json.loads(a['content'])
            print(res['header']['title'])
            print(res['header']['date'].replace('.', '-'))


        return None

    def read_daum_blog_link(self, ft, url):
        result = []

        r = get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        for a in soup.find_all(ft.match_soup_class(['article'])):
            rows = a.findChildren(['th', 'tr'])

        for row in rows:
            cells = row.findChildren('td')
            for cell in cells:
                message = row.text.strip()
                title, user_id = self.get_title_and_user_id(message.strip('\n'))
                print(title, user_id)


    def get_title_and_user_id(self, message):
        temp = message.split()
        return' '.join(temp[:-2]), temp[-1].replace('.', '-')


    def request_search_data(self, ft, req_str, mode='accu'):
        # https://apis.daum.net/search/blog?apikey={apikey}&q=다음&output=json
        url = 'https://apis.daum.net/search/blog?apikey=%s&q=' % (ft.daum_app_key)
        encText = urllib.parse.quote(req_str)
        options = '&result=20&sort=%s&output=json' % mode
        req_url = url + encText + options
        request = urllib.request.Request(req_url)
        try:
            response = urllib.request.urlopen(request)
        except:
            print('[DAUM]search data failed: %s %s' % (req_str, sys.exc_info()[0]))
            return None
        rescode = response.getcode()
        if (rescode == 200):
            response_body = response.read()
            data = response_body.decode('utf-8')
            res = json.loads(data)

            send_msg_list = []
            # http://xxx.tistory.com
            p = re.compile(r'^http://\w+.tistory.com/\d+')
            p2 = re.compile(r'^https://brunch.co.kr/\@\w+/\d+')

            for i in range(len(res['channel']['item'])):
                # title = res["channel"]['item'][i]['title']
                #if (self.check_daum_duplicate(ft, res["channel"]['item'][i]['link'])):
                #    continue  # True
                m = p.match(res["channel"]['item'][i]['link'])
                if m is None:  # other
                    m2 = p2.match(res["channel"]['item'][i]['link'])
                    if m2 is not None: 
                        msg = self.read_other_blog_link(ft, res["channel"]['item'][i]['link'])
                        return None
                    else:
                        print('[other]: ', res["channel"]['item'][i]['link'])
                else:  # tistory blog
                    print('[tistory]: ', res["channel"]['item'][i]['link'])
                    #msg = self.read_daum_blog_link(ft, res["channel"]['item'][i]['link'])

                #send_msg_list.append(res["channel"]['item'][i]['link'])
                #send_msg_list.append("\n".join(msg))

            #send_msg = "\n".join(send_msg_list)
        else:
            print("[DAUM] Error Code: %s" + rescode)
            return None

    def check_daum_duplicate(self, ft, blog_url):
        ret = self.sqlite3.already_sent_daum(blog_url)
        if ret:
            print('Already exist: %s', blog_url)
            return True

        self.sqlite3.insert_daum_blog(blog_url)
        return False


def main():
    ft = FTbot()
    d = UseDaum(ft)
    d.request_search_data(ft, "사람")


if __name__ == '__main__':
    main()
