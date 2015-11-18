#! /usr/bin/env python
#coding=utf-8

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
import sys
sys.path.append("./Chinese_Sentiment_master/")
sys.path.append("./Preprocessing_module")
sys.path.append("./Machine_learning_features")
import jieba
import jieba.analyse
import redis
import re
import chardet
import pickle
import logging
from LDA_classes.ldaFindCategory import *
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
import jieba.posseg as pseg
from gensim import corpora, models, similarities
from gensim.models import ldamodel
reload(sys)
sys.setdefaultencoding('utf-8')


# 袁豪的文件
file_path_train = "/home/acnlp/ldaModel/b"
save_dict = "/home/acnlp/ldaModel/LDA_classes/tmp/dicionary.dict"
save_corpus = "/home/acnlp/ldaModel/LDA_classes/tmp/corpus.mm"
save_lda = "/home/acnlp/ldaModel/LDA_classes/tmp/model.lda"
save_index = "/home/acnlp/ldaModel/LDA_classes/tmp/deerwester.index"
save_doc = "/home/acnlp/ldaModel/LDA_classes/tmp/doc.file"
save_filename = "/home/acnlp/ldaModel/LDA_classes/tmp/filename.file"
save_final = "/home/acnlp/ldaModel/LDA_classes/tmp/final.file"
# files_loc = [os.path.join(root, n) for root, file, name in os.walk(file_path_train) for n in name]
f = open(save_filename, 'rb')
files_loc = pickle.load(f)
f.close()
# classes = ["_".join(item.strip().split("/")[-1].split(".")[0].split("_")[:-1]) for item in files_loc]  # 训练数据的类别
classes = ["_".join(item.strip().split("/")[-1].split(".")[0].split("_")[:-1]) for item in files_loc]  # 训练数据的类别
ldaModel = lda_model(files_loc, classes)
model_file = open(save_final, 'rb')
ldaModel = pickle.load(model_file)
model_file.close()
ldaModel.tfidf_corpus = ldaModel.tfidf[ldaModel.corpus]
print ldaModel.classes
# 袁豪的文件加载完毕


redis_conf = '211.155.92.85'
# redis_conf = '127.0.0.1'
clientReceiver = redis.Redis(host=redis_conf, port=6379, db=1)
clientSender = redis.Redis(host=redis_conf, port=6379, db=1)
receiver = clientReceiver.pubsub()
print('启动监听')

# 订阅频道
receiver.subscribe(['exactCut', 'searchCut', 'kwAnalyse', 'wordFlag', 'sentiments', 'similar','ldaCategory'])

for item in receiver.listen():

    if item['type'] == 'message':

        reqParamList = item['data'].split('!@#')

        if item['channel'] == 'exactCut':

            # 精确分词
            wordList = jieba.cut(reqParamList[1])

            clientSender.publish('cutResult', reqParamList[0] + '!@#' + ','.join(wordList))


        elif item['channel'] == 'ldaCategory':
            doc = reqParamList[1]
            data, data_vec = ldaModel.file_to_vec(doc)
            out_put, out_put_class = ldaModel.pre(data_vec)
            clientSender.publish('sentimentsResult', reqParamList[0] + '!@#' + out_put_class)
