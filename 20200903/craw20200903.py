from bs4 import BeautifulSoup
from konlpy.tag import Kkma
import requests
import datetime
import pymongo


print('Program start')
source = requests.get('https://www.chosun.com/').content
soup = BeautifulSoup(source, 'html.parser', from_encoding='utf-8')
 
div_fusion = soup.find('div', {'id':'fusion-app'})
div_layout_bg = div_fusion.find('div', {'class':'layout--bg box-lg--pad-left-xs box-lg--pad-right-xs'})

for tag in div_layout_bg:
    if tag.name == 'header':
        tag.extract()



# span_list = div_layout_bg.find_all('span')

div_news_list = div_layout_bg.find_all('div', {'class':'story-card-component story-card__headline-container | text--overflow-ellipsis text--left'})

kkma = Kkma()
now = datetime.datetime.now()
today = now.strftime("%Y%m%d%H%M%S")

news_text_list = []
news_list = []
for div_news in div_news_list:
    atag = div_news.find('a')
    span = div_news.find('span')
    news_text = span.text
    href_text = atag['href']
    if href_text.startswith('/'):
        href_text = 'https://www.chosun.com' + href_text
    if len(news_text) > 0:
        ext_list = list(filter(lambda x: x == news_text, news_text_list))
        if len(ext_list) > 0:
            continue
        news_text_list.append(news_text)
        words = kkma.nouns(news_text)
        item = {
            'news_date':today,
            'news_text':news_text,
            'words':words,
            'href': href_text
        }
        news_list.append(item)

for news in news_list:
    print(news['news_text'], news['href'])

if len(news_list) > 0:
    host = 'mongodb://moya:moya2020@ec2-54-180-142-147.ap-northeast-2.compute.amazonaws.com:39091/moya?authSource=admin&readPreference=primary&appname=MongoDB%20Compass%20Community&ssl=false'
    port = 39091

    print('DB insert...')
    connection = pymongo.MongoClient(host)
    database = connection.get_database('moya')
    collection = database.get_collection('news')
    collection.insert_many(news_list)
    connection.close()

print('Program completed.')