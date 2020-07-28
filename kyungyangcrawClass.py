from bs4 import BeautifulSoup
from xCrawling import xCrawling
from CrawType import CrawType
from NewsType import NewsType
import requests
import numpy as np
import pandas as pd
import time

def unionkeys(all_keys, news_list):
    for item in news_list:
        if not item['key'] in all_keys:
            all_keys.append(item['key'])
    return all_keys

def getkeys(news_list):
    ret_list = []
    for item in news_list:
        ret_list.append(item['key'])
    return ret_list

start = time.time()

crawling = xCrawling()
source = requests.get('http://www.khan.co.kr/').content
soup = BeautifulSoup(source, 'html.parser', from_encoding='utf-8')
node1 = soup.find_all('strong', {'class':'hd_title top'})
remove_words = []
okt_news_list = crawling.process(CrawType.Okt, NewsType.Kyungyang, node1, remove_words)
kma_news_list = crawling.process(CrawType.Kkma, NewsType.Kyungyang, node1, remove_words)
han_news_list = crawling.process(CrawType.Hannan, NewsType.Kyungyang, node1, remove_words)
kom_news_list = crawling.process(CrawType.Komor, NewsType.Kyungyang, node1, remove_words)

# print('<<okt>>')
# print(okt_news_list)
# print('<<kma>>')
# print(kma_news_list)
# print('<<han>>')
# print(han_news_list)
# print('<<kom>>')
# print(kom_news_list)

all_keys = []
all_keys = unionkeys(all_keys, okt_news_list)
all_keys = unionkeys(all_keys, kma_news_list)
all_keys = unionkeys(all_keys, han_news_list)
all_keys = unionkeys(all_keys, kom_news_list)

# 교차 확인
print('<< TOP WORDS >>')
topkey_list = []
for key in all_keys:
    find_flag = 0
    list0 = getkeys(okt_news_list)
    list1 = getkeys(kma_news_list)
    list2 = getkeys(han_news_list)
    list3 = getkeys(kom_news_list)
    if key in list0:
        find_flag += 1
    if key in list1:
        find_flag += 1
    if key in list2:
        find_flag += 1
    if key in list3:
        find_flag += 1

    if find_flag > 1:
        print(key, find_flag)
        topkey_list.append(key)

topnews_list = []
for topkey in topkey_list:
    for news in crawling.news_list:
        if str(news).__contains__(topkey):
            items = list(filter(lambda x: x['news'] == news, topnews_list))
            if len(items) > 0:
                items[0]['cnt'] = items[0]['cnt'] + 1
            else:
                topnews_list.append({
                    'news':news,
                    'cnt':1
                })

for topn in topnews_list:
    print('{}'.format(topn))

print('time : {}'.format(time.time() - start))