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
    url = 'http://www.todayhumor.co.kr/board/list.php?kind=search&keyfield=subject&keyword=%s&Submit.x=0&Submit.y=0&Submit=검색' % '시험'
    url = 'http://www.todayhumor.co.kr/board/list.php?kind=search&keyfield=subject&keyword=%s&Submit.x=0&Submit.y=0&Submit=검색' % '사람'
    r = get(url)
    if r.status_code != codes.ok:
        print('[MBN Realesate] request error')
        return None

    # 아, 인코딩이 너무 다르다..
    soup = BeautifulSoup(r.text, 'html.parser')
    #soup = BeautifulSoup(r.content.decode('euc-kr', 'replace'), 'html.parser')
    for l in soup.find_all(match_soup_class(['view'])):
        idx = 0
        temp_url = None
        for o in l.find_all('td'):
            idx += 1
            if idx == 1:
                continue
            #print('idx=', idx, '=>', o.text)
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

            #print('idx=', idx, 'text=', o.text)
            if idx % 7 == 3:  
                print('idx=', idx, 'title=', o.text)
            if idx % 7 == 4:  
                print('idx=', idx, 'id=', o.text)
            if idx % 7 == 5:  
                print('idx=', idx, 'date=', o.text)
                print('idx=', idx, 'url=', url)
                temp_url = None

if __name__ == '__main__':
    main()
