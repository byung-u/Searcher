#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os

from twython import Twython, TwythonError


class FTbot:  # Find the Treasure
    def __init__(self):

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

    def match_soup_class(self, target, mode='class'):
        def do_match(tag):
            classes = tag.get(mode, [])
            return all(c in classes for c in target)
        return do_match


def main():
    ft = FTbot()
    try:
        timeline_pop = ft.twitter.search(
            q='스타벅스', result_type='popular', count=1)
        raw_timeline(ft, timeline_pop)
    except TwythonError as e:
        ft.logger.error('TwythonError %s', e)


def raw_timeline(ft, timeline):
    dump_tl = json.dumps(timeline)  # dict -> json
    tl = json.loads(dump_tl)
    for i in tl['statuses']:
        print('[TEXT]', i['text'])
        print('[CREATED_AT]', i['created_at'])
        for url in i['entities']['urls']:
            print('[MEDIA_URL]', url['url'])
            break  # need 1st url
        print('[USER_ID]', i['user']['screen_name'])
        print('[USER_CREATED_AT]', i['user']['created_at'])


if __name__ == '__main__':
    main()
