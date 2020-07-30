from bs4 import BeautifulSoup
from konlpy.tag import Kkma
import requests
import datetime
import pymongo


print('Program start')
source = requests.get('https://www.chosun.com/').content
soup = BeautifulSoup(source, 'html.parser', from_encoding='utf-8')
node1 = soup.find_all('dl', {'class':'news_item'})

# source = requests.get('https://joongang.joins.com/').content
# soup = BeautifulSoup(source, 'html.parser', from_encoding='utf-8')
# node1 = soup.find_all('ul', {'class':'list_vertical'})

# source = requests.get('https://www.donga.com/').content
# soup = BeautifulSoup(source, 'html.parser', from_encoding='utf-8')
# node1 = soup.find_all('span', {'class':'txt'})

kkma = Kkma()
now = datetime.datetime.now()
today = now.strftime("%Y%m%d%H%M%S")

news_list = []
for node in node1:
    dt_rows = node.find_all('dt')
    for dt in dt_rows:
        news = dt.text.replace('\n', '')
        a = dt.find('a')
        if len(news) > 0:
            words = kkma.nouns(news)
            item = {
                "news_date" : today,
                "news_text" : news,
                "words" : words,
                'href' : a['href']
            }
            news_list.append(item)
    # news = node.text.replace('\n', '')
    # if len(news) > 0:
    #     words = kkma.nouns(news)
    #     item = {
    #         "news_date" : today,
    #         "news_text" : news,
    #         "words" : words
    #     }
    #     news_list.append(item)

for news in news_list:
    print(news)

host = 'ec2-54-180-142-147.ap-northeast-2.compute.amazonaws.com'
port = 27017

print('DB insert...')
connection = pymongo.MongoClient(host, port)
database = connection.get_database('moya')
collection = database.get_collection('news')
collection.insert_many(news_list)
connection.close()
print('Program completed.')