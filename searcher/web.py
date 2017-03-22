# -*- coding: utf-8 -*-
import json
import urllib.request
import re
import sys

from bs4 import BeautifulSoup
from requests import get, codes


def search_web_browsers(s):
    for key in s.keys:
        # get_daum(s, key)
        # get_naver(s, key)
        # get_today_humor(s, key):
        get_ppomppu(s, key)
        return  # TODO : remove after test
    return


def get_today_humor(s, key):
    url = 'http://www.todayhumor.co.kr/board/list.php?kind=search&keyfield=subject&keyword=%s&Submit.x=0&Submit.y=0&Submit=검색' % key
    r = get(url)
    if r.status_code != codes.ok:
        print('[TodayHumor] request error')
        return None

    soup = BeautifulSoup(r.text, 'html.parser')
    for l in soup.find_all(match_soup_class(['table_container'])):
        idx = 0
        for o in l.find_all('td'):
            idx += 1
            if idx == 1:
                continue
            if idx % 7 == 4:
                print('idx=', idx, 'title=', o.text)
            if idx % 7 == 5:
                print('idx=', idx, 'id=', o.text)
            if idx % 7 == 6:
                print('idx=', idx, 'date=', o.text)


def get_ppomppu(s, key):
    url = 'http://www.todayhumor.co.kr/board/list.php?kind=search&keyfield=subject&keyword=%s&Submit.x=0&Submit.y=0&Submit=검색' % '사람'
    #url = 'http://www.ppomppu.co.kr/search_bbs.php?keyword=%s' % key
    r = get(url)
    if r.status_code != codes.ok:
        s.logger.error('[Oh_U] Error Code: %d', rescode)
        return None
    soup = BeautifulSoup(r.text, 'html.parser')
    #soup = BeautifulSoup(r.content.decode('utf-8r', 'replace'), 'html.parser')
    #soup = BeautifulSoup(r.content.decode('euc-kr', 'ignore'), 'html.parser')
    print(soup)


def get_naver(s, key, mode='blog'):
    url = 'https://openapi.naver.com/v1/search/%s?query=' % mode
    encText = urllib.parse.quote(key)
    options = '&display=20&sort=date'
    req_url = url + encText + options
    request = urllib.request.Request(req_url)
    request.add_header('X-Naver-Client-Id', s.naver_client_id)
    request.add_header('X-Naver-Client-Secret', s.naver_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if (rescode != 200):
        s.logger.error('[NAVER] Error Code: %d', rescode)
        return None
    response_body = response.read()
    data = response_body.decode('utf-8')
    js = json.loads(data)
    items = int(js["display"])
    #print(items, type(items))
    for i in range(0, items):
        print(js["items"][i]["title"])
        page_num = get_naver_blog_page_num(js["items"][i]["link"])
        naver_blog_link = '%s/%s' % (js["items"][i]["bloggerlink"], page_num)
        print(naver_blog_link)
        print(js["items"][i]["description"])
    return 

def get_naver_blog_page_num(naver_blog_link):
    temp_link = naver_blog_link.split('=')
    return temp_link[-1]

def get_daum(s, key, mode='accu'):

    # https://apis.daum.net/search/blog?apikey={apikey}&q=다음&output=json
    url = 'https://apis.daum.net/search/blog?apikey=%s&q=' % (s.daum_app_key)
    encText = urllib.parse.quote(key)
    options = '&result=20&sort=%s&output=json' % mode
    req_url = url + encText + options
    request = urllib.request.Request(req_url)
    try:
        response = urllib.request.urlopen(request)
    except:
        s.logger.error('[DAUM]error: %s %s',
                       key, sys.exc_info()[0])
        return None
    rescode = response.getcode()
    if (rescode != 200):
        s.logger.error('[DAUM] Error Code: %d', rescode)
        return None

    # http://xxx.tistory.com
    p = re.compile(r'^http://\w+.tistory.com/\d+')

    send_msg = []
    response_body = response.read()
    data = response_body.decode('utf-8')
    res = json.loads(data)
    for i in range(len(res['channel']['item'])):
        # title = res["channel"]['item'][i]['title']
        daum_blog_link = res["channel"]['item'][i]['link']
        if (s.check_duplicate_item(daum_blog_link, 'daum')):
            continue  # True duplicated
        m = p.match(daum_blog_link)
        if m is None:  # other
            msg = read_daum_blog_link(s, daum_blog_link, 'other')
        else:  # tistory blog
            msg = read_daum_blog_link(s, daum_blog_link, 'tistory')
        send_msg.append(daum_blog_link)
        send_msg.append("\n".join(msg))
    print(send_msg)
    return


def read_daum_blog_link(s, daum_blog_link, mode):
    result = []
    r = get(daum_blog_link)
    soup = BeautifulSoup(r.text, 'html.parser')
    if mode == 'other':
        for a in soup.find_all(s.match_soup_class(['view'])):
            for p in soup.find_all('p'):
                if len(p.text.strip()) == 0:
                    continue
                result.append(p.text.replace('\n', ' ').strip())
        return result
    else:
        for a in soup.find_all(s.match_soup_class(['article'])):
            for p in soup.find_all('p'):
                if len(p.text.strip()) == 0:
                    continue
                if p.text.find('adsbygoogle') >= 0:
                    continue
                result.append(p.text.strip())

        for a in soup.find_all(s.match_soup_class(['area_view'])):
            for p in soup.find_all('p'):
                if len(p.text.strip()) == 0:
                    continue
                if p.text.find('adsbygoogle') >= 0:
                    continue
                result.append(p.text.strip())
        return result
