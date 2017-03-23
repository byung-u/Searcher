# -*- coding: utf-8 -*-
import json
import urllib.request
import re
import sys

from bs4 import BeautifulSoup
from requests import get, codes

from searcher.google_sheet import append_google_sheet


def search_webs(s):
    for key in s.keys:
        # get_daum(s, key)
        # get_naver(s, key)
        get_today_humor(s, key)
        # get_ppomppu(s, key)
        return  # TODO : remove after test
    return


def get_today_humor(s, key):
    url = 'http://www.todayhumor.co.kr/board/list.php?kind=search&keyfield=subject&keyword=%s&Submit.x=0&Submit.y=0&Submit=검색' % key
    r = get(url)
    if r.status_code != codes.ok:
        s.logger.error('[TodayHumor] request error')
        return None

    soup = BeautifulSoup(r.text, 'html.parser')
    for l in soup.find_all(s.match_soup_class(['view'])):
        idx = 0
        temp_url = None
        for o in l.find_all('td'):
            idx += 1
            if idx == 1:
                continue
            # print('idx=', idx, '=>', o.text)
            try:
                o.a['href']
                if temp_url is None:
                    temp_url = o.a['href']
                    u = re.search('(.*)&keyfield(.*)', temp_url)
                    if u is None:
                        temp_url = None
                    else:
                        url = 'http://www.todayhumor.co.kr%s' % u.group(1)
            except TypeError:
                pass
            # print('idx=', idx, 'text=', o.text)
            if idx % 7 == 3:
                title = o.text
            if idx % 7 == 4:
                user_id = o.text
            if idx % 7 == 5:
                temp_date = o.text
                temp_date = temp_date.replace('/', '-')
                rm_hm = temp_date.split()  # rm hour, minute
                post_date = '20%s' % rm_hm[0]

                append_google_sheet(s, user_id, url, title, post_date, '오늘의 유머')
                user_id, url, title, post_date = None, None, None, None
                temp_url = None
    return None


def get_ppomppu(s, key):
    url = 'http://www.todayhumor.co.kr/board/list.php?kind=search&keyfield=subject&keyword=%s&Submit.x=0&Submit.y=0&Submit=검색' % '사람'
    # url = 'http://www.ppomppu.co.kr/search_bbs.php?keyword=%s' % key
    r = get(url)
    if r.status_code != codes.ok:
        s.logger.error('[Oh_U] request error')
        return None
    soup = BeautifulSoup(r.text, 'html.parser')
    # soup = BeautifulSoup(r.content.decode('utf-8r', 'replace'), 'html.parser')
    # soup = BeautifulSoup(r.content.decode('euc-kr', 'ignore'), 'html.parser')
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
    for i in range(0, items):
        # http://blog.naver.com/ecampus_kgu?Redirect=Log&amp;logNo=220965327425
        page_num = get_naver_blog_page_num(js["items"][i]["link"])
        # http://blog.naver.com/ecampus_kgu
        user_id = get_naver_blog_user_id(js["items"][i]["bloggerlink"])
        naver_blog_link = '%s/%s' % (js["items"][i]["bloggerlink"], page_num)
        post_date = get_naver_blog_post_date(js["items"][i]["postdate"])
        # print(js["items"][i]["description"])
        title = js["items"][i]["title"]
        append_google_sheet(s, user_id, naver_blog_link, title, post_date,
                            'naver', 'blog')
    return


def get_naver_blog_page_num(naver_blog_inner_link):
    temp_link = naver_blog_inner_link.split('=')
    return temp_link[-1]


def get_naver_blog_user_id(naver_blog_link):
    u = re.search(r'^http://blog.naver.com/(.*)', naver_blog_link)
    return u.group(1)


def get_naver_blog_post_date(post_date):  # 20170323 -> 2017-03-23
    return '-'.join([post_date[:4], post_date[4:6], post_date[6:]])


def get_daum(s, key, mode='date'):

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
    p1 = re.compile(r'^http://\w+.tistory.com/\d+')
    # http://brunch.co.kr/@xxx/x
    p2 = re.compile(r'^https://brunch.co.kr/\@\w+/\d+')

    response_body = response.read()
    data = response_body.decode('utf-8')
    res = json.loads(data)
    for i in range(len(res['channel']['item'])):
        # title = res["channel"]['item'][i]['title']
        daum_blog_link = res["channel"]['item'][i]['link']
        # TODO : add duplicated check all functions at once.
        # if (s.check_duplicate_item(daum_blog_link, 'daum')):
        #     continue  # True duplicated
        m = p1.match(daum_blog_link)
        if m:
            user_id = re.search(r'^http://(.*).tistory.com/\d+', daum_blog_link)
            title, post_date = parse_tistory_page(s, daum_blog_link)
            if title is None or post_date is None:
                continue
            append_google_sheet(s, user_id, daum_blog_link, title, post_date,
                                'daum', 'blog')
        else:
            m = p2.match(daum_blog_link)
            if m:
                user_id = re.search('https://brunch.co.kr/\@(.*)/\d+', daum_blog_link)
                title, post_date = parse_brunch_page(daum_blog_link)
                if title is None or post_date is None:
                    continue
                append_google_sheet(s, user_id, daum_blog_link, title, post_date,
                                    'daum', 'blog')
            else:
                print('[else]', daum_blog_link)  # drop
    return


def parse_tistory_page(s, daum_blog_link):
    r = get(daum_blog_link)
    soup = BeautifulSoup(r.text, 'html.parser')
    rows = None
    for a in soup.find_all(s.match_soup_class(['article'])):
        rows = a.findChildren(['th', 'tr'])

    if rows is None:
        return None, None

    for row in rows:
        cells = row.findChildren('td')
        for cell in cells:
            message = row.text.strip()
            return get_title_and_user_id(message.strip('\n'), 'tistory')
    return None, None


def parse_brunch_page(daum_blog_link):
        r = get(daum_blog_link)
        soup = BeautifulSoup(r.text, 'html.parser')
        for a in soup.find_all('meta', property="ks:richscrap"):
            res = json.loads(a['content'])
            return (res['header']['title'], res['header']['date'].replace('.', '-'))


def get_title_and_user_id(message, blog_type=None):
    if blog_type == 'tistory':
        temp = message.split()
        return' '.join(temp[:-2]), temp[-1].replace('.', '-')
    else:
        print('invalid blog_type: ', blog_type)
        return None, None
