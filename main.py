from konlpy.tag import Okt
from konlpy.tag import Kkma
import pandas as pd
from bs4 import BeautifulSoup
import requests

# source = requests.get('https://joongang.joins.com/').content
# soup = BeautifulSoup(source, 'html.parser', from_encoding='utf-8')
# node1 = soup.find_all('ul', {'class':'list_vertical'})

source = requests.get('https://www.chosun.com/').content
soup = BeautifulSoup(source, 'html.parser', from_encoding='utf-8')
node1 = soup.find_all('dl', {'class':'news_item'})
for node in node1:
    print(node.text)







# org_text = '마음건강길 오프라 원프리, 치질연고를 얼굴에 발랐다고? 왜?'

# okt = Okt()
# text = okt.pos(org_text)
# print(text)

# kkma = Kkma()
# text2 = kkma.pos(org_text)
# print(text2)
# text3 = kkma.nouns(org_text)
# print(text3)





# arr = []

# arr.append({'key' : 'a', 'val' : 100 })
# arr.append({'key' : 'b', 'val' : 200 })
# arr.append({'key' : 'c', 'val' : 300 })
# arr.append({'key' : 'd', 'val' : 400 })

# search = list(filter(lambda x: x['key'] == 'c', arr))
# search[0]['val'] = 700

# print(arr)