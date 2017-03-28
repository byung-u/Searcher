#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup
from requests import get, codes


def match_soup_class(target, mode='class'):
    def do_match(tag):
        classes = tag.get(mode, [])
        return all(c in classes for c in target)
    return do_match


def main():
    url = 'http://pann.nate.com/search?searchType=A&q=%s' % '사람'
    r = get(url)
    if r.status_code != codes.ok:
        print('[MBN Realesate] request error')
        return None

    soup = BeautifulSoup(r.text, 'html.parser')
    for sr in soup.find_all(match_soup_class(['srch_list'])):
        rows = sr.findChildren(['dt', 'dl'])

        for row in rows:
            cells = row.findChildren('dt')
            for cell in cells:
                # user_id, title, date
                #print(row.a['href'])
                temp = row.find(match_soup_class(['info']))
                print(temp)
                print('\n\n')
                info = row.text.strip().split('\n')
                title = info[0]
                date = info[-1].replace('.', '-')
                user_id, post_date = get_nate_id_and_date(date, info[-2])
                


def get_nate_id_and_date(date, user_info):
    if len(date) == len('17-03-23'):
        post_date='20%s' % date
        return post_date, user_info
    else:
        u1 = re.search('(.*)이야기(.*) ', date)
        if u1 is not None:  # 10대 이야기I__D17-03-23 02:18
            u2 = re.search('(.*)-(.*)-(.*)', u1.group(2))  # I__D17-03-23
            user_id_year = (u2.group(1)) # I__D17
            user_id = user_id_year[:-2]  # I__D
            year = user_id_year[-2:]     # 17
            post_date = '20%s-%s-%s' % (year, u2.group(2), u2.group(3))
            return user_id, post_date
        else:  # 아이디17-03-23 00:10
            u2 = re.search('(.*)-(.*)-(.*) ', date)  # 아이디17-03-23
            user_id_year = (u2.group(1))  # 아이디17
            user_id = user_id_year[:-2]   # 아이디
            year = user_id_year[-2:]  # 17
            post_date = '20%s-%s-%s' % (year, u2.group(2), u2.group(3))
            return user_id, post_date
    return None, None
'''
20대 이야기ㅋㅋㅋㅋ17-03-23 01:09
ㅇㅇ17-03-20 19:54
17-03-23
'''
    

if __name__ == '__main__':
    main()
