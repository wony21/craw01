# https://www.donga.com/

from bs4 import BeautifulSoup
from konlpy.tag import Okt
from konlpy.tag import Kkma
from konlpy.tag import Hannanum
from konlpy.tag import Komoran
import woorimal as woori
import operator
import requests
import re
import time

# def news_text_trim(text):
#     # return text.replace('"', '').replace('.', '').replace('#', '').replace('\'', '').replace('·', ' ')
#     # return text.replace('"', '').replace('.', '').replace('#', '')
#     pass

# def news_clean_text(text):
#     pattern = '[^\w\s]'
#     repl = ''
#     ret_text = re.sub(pattern=pattern, repl=repl, string=text)
#     return ret_text

start = time.time()
komor = Komoran()
hannan = Hannanum()
kkma = Kkma()
okt = Okt()
source = requests.get('https://www.donga.com/').content
soup = BeautifulSoup(source, 'html.parser', from_encoding='utf-8')

# top news
# top_news = soup.find('div', {'class' : 'top_news'} )
# top_news_title = top_news.find('span', {'class' : 'center_tit'})
# print('### Top News ###')
# print(top_news_title.text)

# news item
node1 = soup.find_all('span', {'class':'txt'})
news_list = []
keylist = []
for node1_var in node1:
    # news_text : 기사문글
    news_text = node1_var.text.strip().replace('\n', '')
    # kewords : 단어 리스트
    keywords = komor.nouns(news_text)
    # news_list 생성
    news_item = {
        'news' : news_text,
        'keywords' : keywords
    }
    news_list.append(news_item)

    # 단어들의 Rank 구하기
    for key in keywords:
        #if not woori.ignore_keyword(key):
        items = list(filter(lambda x: x['key'] == key, keylist))
        if len(items) > 0:
            items[0]['count'] = items[0]['count'] + 1
        else:
            keylist.append({'key' : key, 'count' : 1 })


sorted_keylist = sorted(keylist, reverse=True, key=lambda k: k['count'])
rank = 0
list2 = []
for item in sorted_keylist:
    #print('<<< {} {} >>>'.format(item['key'], item['count']))
    for news in news_list:
        if item['key'] in news['keywords']:
            #print(news['news'], news['keywords'])
            ext_list = list(filter(lambda x: x['news'] == news['news'], list2))
            if len(ext_list) == 0:
                words = []
                words.append(item['key'])
                list_item = {
                    'key' : item['key'],
                    'news' : news['news'],
                    'words' : words
                }
                list2.append(list_item)
            else:
                for ext in ext_list:
                    ext['words'].append(item['key'])

# 최종 순위 판정
rank_words = []
for item2 in list2:
    print(item2)
    rank_contains = list(filter(lambda x: x['key'] == item2['key'], rank_words))
    if len(rank_contains) > 0:
        rank_contains[0]['count'] = rank_contains[0]['count'] + 1
    else:
        rank_item = {
            'key' : item2['key'],
            'count' : 1
        }
        rank_words.append(rank_item)
    # print('[' + item2['key'] + ']', item2['news'], item2['words'])
sort_list = sorted(rank_words, reverse=True, key=lambda k: k['count'])

rank = 0
for item in sort_list:
    print(item['key'], item['count'])
    rank += 1
    if rank > 10:
        break

print('time : {}'.format(time.time() - start))

