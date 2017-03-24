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
    url = 'http://agora.media.daum.net/nsearch/total?query=%s' % '사람'
    r = get(url)
    if r.status_code != codes.ok:
        print('[Daum Agora] request error')
        return None

    soup = BeautifulSoup(r.text, 'html.parser')
    for sre in soup.find_all(match_soup_class(['sResult'])):
        rows = sre.findChildren(['dt', 'dl'])
        for row in rows:
            cells = row.findChildren('dt')
            for cell in cells:
                # print(row.a.text) # title
                # #print(row.a['href'])  # url
                date = row.find(match_soup_class(['date']))
                temp_date = date.text.split(' ')
                post_date = temp_date[0].replace('.', '-')
                if post_date.startswith('2') == False:
                    continue

                for a_tag in row.find_all('a'):
                    user_id = a_tag.text  # last text is user_id, so overwrite.
                print(user_id.strip())

'''
<dl>
<dt><a href="http://bbs1.agora.media.daum.net/gaia/do/debate/read?bbsId=D115&amp;articleId=3941859" target="_agora">★ 문재인이란 <b>사람</b>을 알아보고 까라는 삼등시민아..</a> <span class="date">2017.03.22 (수) 오후 17:49</span></dt>
<dd class="txt">대선 왜, 문재인이 아닌 이재명이어야 하는가? 아래기사에서 언급하지 않은 것... 문재인, 박근혜, 이재용 세 <b>사람</b> 모두 동일하게 자신들이 능력이 있다는 것을 아무것도 증명하지 못했다는 것. 그리고 현재 대선주자로서...
				<p class="node">
<a href="debate?query=%EC%82%AC%EB%9E%8C&amp;board_id=43079">경제</a>
<span class="bar">|</span>
<a href="http://agora.media.daum.net/my/list?key=SZrWYM5puUY0&amp;group_id=1" target="_agora"> 이니그마</a>
</p></dd>
</dl>
<dl class="thum">
<dd class="img"><a href="http://bbs1.agora.media.daum.net/gaia/do/debate/read?bbsId=D101&amp;articleId=5515204" target="_agora"><img alt="" src="http://img1.daumcdn.net/thumb/W100x100/?fname=http%3A%2F%2Fi1.media.daumcdn.net%2Fuf%2Fimage%2FU01%2Fagora%2F58B016994156DD001E"/></a></dd>
<dt><a href="http://bbs1.agora.media.daum.net/gaia/do/debate/read?bbsId=D101&amp;articleId=5515204" target="_agora">[19禁] 실종자2372명. 왜 해마다 <b>사람</b>들이 증발하는가?</a> <span class="date">2017.02.24 (금) 오후 20:19</span></dt>
<dd class="txt">이건 지난 통계이지만, 2011년 한해동안 실종신고가 3만건 이상 접수가 되었고, 1년동안 찾지못한 <b>사람</b>수가 무려 2372명이라고 합니다. 성인인데 실종되는 건수가 이정도로 많다면, 이건 일종의 범죄조직에 연루되어 실종된...
				<p class="node">
<a href="debate?query=%EC%82%AC%EB%9E%8C&amp;board_id=6">정치</a>
<span class="bar">|</span>
<a href="http://agora.media.daum.net/my/list?key=lllQdVUYBFY0&amp;group_id=1" target="_agora"> presumptuous</a>
</p></dd>
</dl>
<dl>
<dt><a href="http://bbs3.agora.media.daum.net/gaia/do/story/read?bbsId=K161&amp;articleId=574049" target="_agora">온누리교회 다니는<b>사람</b> 보세요 이<b>사람</b> 사기꾼입니다</a> <span class="date">2017.03.23 (목) 오후 23:38</span></dt>
<dd class="txt">하며 사는 그ㅈ ㅣ ㅆㄲ 이 사기꾼 절대 용서 할수가 없네요 이천만원 돈을 떠나서 배신감에 용서할수가 없어요 저는 지금 인생 정리중입니다 이 사기꾼 어떻게 되는지 보세요 ▲ 아리화장품 송동운 대표 이<b>사람</b> 사기꾼입니다
				<p class="node">
<a href="story?query=%EC%82%AC%EB%9E%8C&amp;board_id=8">수다</a>
<span class="bar">|</span>
<a href="http://agora.media.daum.net/my/list?key=5ysneIQG3H90&amp;group_id=1" target="_agora"> KWC</a>
</p></dd>
</dl>
'''
                


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
