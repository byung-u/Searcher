#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def insert_google_sheet(s, searched):

    # https://developers.google.com/sheets/guides/concepts
    print('[ADD]', searched)

    rangeName = 'A3:A'  # start line
    # values = {'values':[['Hello Saturn',],]}
    # values = {'values': [['2', '', 'ak홍길동', '', '2016-07-06', '2016-07-06', 'http://cafe.daum.net/3664175/3vE/1029', '', '네이버', '카페', '1'],]}
    # searched = ['3', '', 'sssak홍길동', '', '2016-07-06', '2016-07-06', 'http://cafe.daum.net/3664175/3vE/1029', '', '네이버', '카페', '1']
    values = {'values': [searched, ]}
    s.service.spreadsheets().values().append(
        spreadsheetId=s.spreadsheetId, range=rangeName,
        valueInputOption='RAW', body=values).execute()

    """  # debug
    rangeName = 'Sheet1!A3:L'
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])
    if not values:
        print('No data found.')
    else:
        for row in values:
            print(row)
    """
    return


def get_last_index(s):
    rangeName = 'temp_sheet!A3:O'
    result = s.service.spreadsheets().values().get(
        spreadsheetId=s.spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])
    if not values:
        s.logger.error('Data not found')
        return 0
    else:
        idx = 0
        for row in values:
            idx = int(row[0])
    return idx


def append_google_sheet(s, user_id, link, title, date, web_type, web_sub_type=None):

    duplicate = s.check_duplicate_url(web_type, link)
    if (duplicate):  # True
        s.logger.info('[Duplicated] %s', link)
        print('[duplicated]', link)
        return

    searched_msg = []
    last_idx = get_last_index(s)
    # values = {'values': [['2', '', 'ak홍길동', '', '2016-07-06', '2016-07-06', 'http://cafe.daum.net/3664175/3vE/1029', '', '네이버', '카페', '1'],]}

    searched_msg.append(last_idx + 1)
    searched_msg.append('')
    searched_msg.append(s.operator_name)
    searched_msg.append('')
    searched_msg.append(s.today)
    searched_msg.append(date)  # posted date
    searched_msg.append(link)  # posted url
    searched_msg.append('')
    searched_msg.append(web_type)  # naver, daum, ...
    searched_msg.append(web_sub_type)  # cafe, blog, ...
    searched_msg.append('1')  # default
    searched_msg.append('')
    searched_msg.append('')
    searched_msg.append('')
    searched_msg.append(user_id)

    insert_google_sheet(s, searched_msg)
