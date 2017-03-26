#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re


def main():
    url = 'https://brunch.co.kr/@kimhanbyul/20'
    p2 = re.compile(r'^https://brunch.co.kr/\@\w+/\d+')
    m = p2.match(url)
    if m:
        print('got it')
    else:
        print('nope')

    url = 'asdf=5;iwantthis123jasd'
    u = re.search('asdf=5;(.*)123jasd', url)
    print(u.group(1))
    
    url = 'https://brunch.co.kr/@kimhanbyul/20'
    u = re.search('https://brunch.co.kr/\@(.*)/\d+', url)
    print(u.group(1))


    url = 'http://jinny1970.tistory.com/2043'
    u = re.search(r'^http://(.*).tistory.com/\d+', url)
    print(u.group(1))

    url = 'http://blog.naver.com/delete74123'
    u = re.search(r'^http://blog.naver.com/(.*)', url)
    print(u.group(1))


    url = '/board/view.php?table=bestofbest&no=313990&s_no=313990&no_tag=1&kind=search&page=1&keyfield=subject&keyword=%EC%82%AC%EB%9E%8C'
    u = re.search('(.*)&keyfield(.*)', url)
    print(u.group(1))
    print(u.group(2))
    print('\n\n\n')

    date = '10대 이야기ㅇzzz17-03-23 02:18'
    date = '17-03-23'
    date = 'ㅇㅇ17-03-23 00:10'
    if len(date) == len('17-03-23'):
        post_date='20%s' % date
        print(post_date)
    else:
        u = re.search('(.*)이야기(.*) ', date)
        if u is not None:  # 10대 이야기I__D17-03-23 02:18
            u2 = re.search('(.*)-(.*)-(.*)', u.group(2))
            user_id_year = (u2.group(1))
            user_id = user_id_year[:-2]
            year = user_id_year[-2:]
            print(user_id)
            post_date = '20%s-%s-%s' % (year, u2.group(2), u2.group(3))
            print(post_date)
        else:  # 아이디17-03-23 00:10
            #temp_date = date.split()
            #u2 = re.search('(.*)-(.*)-(.*)', temp_date[0])
            u2 = re.search('(.*)-(.*)-(.*) ', date)
            user_id_year = (u2.group(1))
            user_id = user_id_year[:-2]
            year = user_id_year[-2:]
            print(user_id)
            post_date = '20%s-%s-%s' % (year, u2.group(2), u2.group(3))
            print(post_date)
    

    date = '09:32:23'
    date = '09-32-23'
    p = re.compile(r'^\d+:\d+:\d+')
    m = p.match(date)
    if m is None:
        print('not match')
    else:
        print('match')

if __name__ == '__main__':
    main()
