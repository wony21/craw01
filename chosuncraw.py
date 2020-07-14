from bs4 import BeautifulSoup
from konlpy.tag import Okt
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
okt = Okt()
source = requests.get('https://www.chosun.com/').content
soup = BeautifulSoup(source, 'html.parser', from_encoding='utf-8')

# top news
# top_news = soup.find('div', {'class' : 'top_news'} )
# top_news_title = top_news.find('span', {'class' : 'center_tit'})
# print(top_news_title.text)

# news item
node1 = soup.find_all('dl', {'class':'news_item'})
news_list = []
keylist = []
for node1_var in node1:
    # news_text : 기사문글
    news_text = ''
    # kewords : 단어 리스트
    keywords = []
    # a link에 대한 문구
    a = node1_var.find('a')
    if a:
        news_text = a.text.strip().replace('\n', '')
        keywords = okt.nouns(news_text)
    # img에 대한 문구
    img = node1_var.find('img')
    if img:
        if img.has_attr('alt'):
            news_text = img['alt'].strip().replace('\n', '')
            keywords = okt.nouns(news_text)
    # news_list 생성
    news_item = {
        'news' : news_text,
        'keywords' : keywords
    }
    news_list.append(news_item)

    # 단어들의 Rank 구하기
    for key in keywords:
        if not woori.ignore_keyword(key):
            items = list(filter(lambda x: x['key'] == key, keylist))
            if len(items) > 0:
                items[0]['count'] = items[0]['count'] + 1
            else:
                keylist.append({'key' : key, 'count' : 1 })

# keyword의 전체 합 구하기
# for news in news_list:
#     ranksum = 0
#     rankmax = 0
#     for word in news['keywords']:
#         items = list(filter(lambda x: x['key'] == key, keylist))
#         if len(items) > 0:
#             ranksum += items[0]['count']
#             if rankmax < items[0]['count']:
#                 rankmax = items[0]['count']
#     news['rankmax'] = int(rankmax)
#     news['ranksum'] = float(ranksum / len(news['keywords']))
# rank_list = sorted(news_list, reverse=True, key=lambda k: (k['rankmax'], k['ranksum']))

sorted_keylist = sorted(keylist, reverse=True, key=lambda k: k['count'])
rank = 0
for item in sorted_keylist:
    print('{} {}'.format(item['key'], item['count']))
    rank += 1
    if rank > 5:
        break

for news in rank_list:
    print(news)

print('time : {}'.format(time.time() - start))

# # Rank
# print('>>> rank <<<')
# sort_keylist = sorted(keylist.items(), reverse=True, key=operator.itemgetter(1))
# rank_index = 0
# rank_list = []
# for key, value in sort_keylist:
#     print(key, value)
#     rank_index += 1
#     rank_list.append({ 'rankey' : key })
#     if rank_index > 3:
#         break

# # 관련기사 추출
# print('>>> news <<<')
# for rank in rank_list:
#     print('issue : {}'.format(rank))
#     for news in news_list:
#         keywords = news['keywords']
#         if rank['rankey'] in keywords:
#             print(news['news'])

