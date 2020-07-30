from bs4 import BeautifulSoup
from konlpy.tag import Kkma
import requests
import datetime
import pymongo


request = requests.get('https://www.chosun.com/')
with open('output_donga.html', 'w', 'utf-8') as f:
    f.write(request.content)
    f.close()
