#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

def month_converter(month):
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    return months.index(month) + 1

def main():
    now = datetime.now()
    today = '%4d-%02d-%02d' % (now.year, now.month, now.day)
    print(today)

    date_str = '17/03/12 04:14'
    date_str = date_str.replace('/', '-')
    new_date = date_str.split()
    date = '20%s' % new_date[0]
    print(date)

    date_str = 'Tue Mar 1 23:37:29 +0000 2017'
    new_date = date_str.split()
    print(new_date[5])
    print(new_date[2])
    post_date = '%s-%02d-%02d' % (new_date[5], month_converter(new_date[1]), int(new_date[2]))
    print(post_date)

    date = '2017-03-23'
    cmp_date = '2016-03-23'
    print(date[:4])
    if cmp_date.startswith(date[:4]):
        print('match')
    else:
        print('not match')

if __name__ == '__main__':
    main()
