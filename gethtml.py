from bs4 import BeautifulSoup
#from konlpy.tag import Kkma
import requests
import datetime
import pymongo



#response = requests.get('https://www.chosun.com/')
response = requests.get('https://www.donga.com/')
#print(response.status_code)
#print(response.text)
if response.status_code == 200:
    f = open('output_donga.html', 'w', encoding='utf-8')
    f.write(response.text)
    f.close()
