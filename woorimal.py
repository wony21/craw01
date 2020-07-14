# https://stdict.korean.go.kr/openapi/openApiInfo.do
# 597CBCDA56424FEAEBB919B803AD1DE1
# ID : moya  Password : ja2~~~~~#4
import requests
import xml.etree.ElementTree as elemTree

api = 'https://stdict.korean.go.kr/api/search.do'
api_key = '597CBCDA56424FEAEBB919B803AD1DE1'

def ignore_keyword(word):
    api_param = 'key={}&method={}&start={}&num={}&advanced={}&pos={}&q={}'.format(api_key, 'exact', 1, 10, 'n', 2, word)
    response = requests.get('{}?{}'.format(api, api_param))
    response_xml = response.text
    xml = elemTree.fromstring(response_xml)
    for node in xml.findall('./item'):
        pos_node = node.find('./pos')
        # sen_node = node.find('./sense')
        # def_node = sen_node.find('./definition')
        # print(pos_node.text, ':', def_node.text)
        if pos_node.text == '대명사':
            return True
        elif pos_node.text == '조사':
            return True
    return False
    
