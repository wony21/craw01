import pandas as pd
import pymongo
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules
from gensim.models import Word2Vec
import matplotlib.pyplot as plt

# https://ebbnflow.tistory.com/153

# dataset = [['Milk', 'Onion', 'Nutmeg', 'Eggs', 'Yogurt'],
#            ['Onion', 'Nutmeg', 'Eggs', 'Yogurt'],
#            ['Milk', 'Apple', 'Eggs'],
#            ['Milk', 'Unicorn', 'Corn', 'Yogurt'],
#            ['Corn', 'Onion', 'Onion', 'Ice cream', 'Eggs']]


# dataset = [['정부', '의협', '합의', '합의문', '문', '서명', '전', '전공의', '공의', '안해', '파업', '계속'], 
#            ['위기', '위기때', '때', '여권'], 
#            ['의사', '간호사', '임대인', '임차인', '국민', '정부'], 
#            ['해일', '시장', '침수', '교량', '유', '유실태', '실태', '마', '마이삭', '이삭', '피해', '속출'], 
#            ['대통령', '의사', '간호사', '편', '비난', '댓', '댓글', '글', '폭주']]

# dataset = [['가','나','다'],['나','다','라'],['가','다','라'],['나','다']]
# dataset=[['사과','치즈','생수'],
# ['생수','호두','치즈','고등어'],
# ['수박','사과','생수'],
# ['생수','호두','치즈','옥수수']]

host = 'mongodb://moya:moya2020@ec2-54-180-142-147.ap-northeast-2.compute.amazonaws.com:39091/moya?authSource=admin'
connection = pymongo.MongoClient(host)
database = connection.get_database('moya')
news_db = database.get_collection('news')
news = news_db.find({ 'news_date' : { '$gte' :'202009041000'} })
dataset = []
href_list = []
for new in news:
    ext_href_list = list(filter(lambda x: x == new['href'], href_list))
    if len(ext_href_list) > 0:
        continue
    href_list.append(new['href'])
    dataset.append(new['words'])
    
connection.close()

print('dataset count', len(dataset))
print(dataset)

# APRIORI 방식
# te = TransactionEncoder()
# te_ary = te.fit(dataset).transform(dataset)
# df = pd.DataFrame(te_ary, columns=te.columns_)
# print(df)
# frequent_itemsets = apriori(df, min_support=1, use_colnames=True)
# print(frequent_itemsets)

# gensim 방식 (Word2Vec)
model = Word2Vec(dataset, size=300, window=3, min_count=0.5, workers=1)
word_vectors = model.wv
vocabs = word_vectors.vocab.keys()
word_vectors_list = [word_vectors[v] for v in vocabs]
result_text = ''
text_center = input('입력:')
for text in dataset:
    #print(text)
    for word in text:
        sim = word_vectors.similarity(w1=text_center,w2=word)
        #print('[' + text_center + ']','과', '[' + word + ']', '연관도',sim)
        result_text += word + ' ' + str(sim) + '\n'
f = open('result.txt', 'w', encoding='utf-8')
f.write(result_text)
f.close()

# from sklearn.decomposition import PCA
# pca = PCA(n_components=2)
# xys = pca.fit_transform(word_vectors_list)
# xs = xys[:,0]
# ys = xys[:,1]

# model.save('word2vec.model')

# model = Word2Vec.load('word2vec.model')

# print(word_vectors.similarity(w1='대통령',w2='코로나'))



