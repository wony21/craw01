import pymongo
import json
from gensim.models import Word2Vec
from flask import Flask
from flask import jsonify
app = Flask(__name__)

@app.route('/')
def home_controller():
    return 'Home'

@app.route('/word2vec/<word>')
def word2vec(word):
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

    model = Word2Vec(dataset, size=300, window=3, min_count=0.5, workers=1)
    word_vectors = model.wv
    vocabs = word_vectors.vocab.keys()
    word_vectors_list = [word_vectors[v] for v in vocabs]
    text_center = word
    result_list = []
    for text in dataset:
        #print(text)
        for word in text:
            sim = word_vectors.similarity(w1=text_center,w2=word)
            #print('[' + text_center + ']','과', '[' + word + ']', '연관도',sim)
            result_list.append({ 'word':word, 'sim': float(sim) })
    return jsonify(result_list)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)