#! /usr/bin/env python
#coding=utf-8

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
import sys
sys.path.append("./Chinese-Sentiment-master/")
sys.path.append("./Preprocessing-module")
sys.path.append("./Machine-learning-features")
import codecs
import jieba
import jieba.analyse
import jieba.posseg as pseg
import redis


#情感
import pos_neg_senti_dict_feature as pn
import textprocessing as tp
#情感with机器学习
import pos_neg_ml_feature as pos_neg_ml

from gensim import corpora, models, similarities

reload(sys)
sys.setdefaultencoding('utf-8')

#jieba分词多进程默认4
# jieba.enable_parallel(4)
# project_path = '/Users/shenxu/Workspace/nlp/'
project_path = './'
docpath='/home/workspace/news'

stopwords = codecs.open(project_path + 'stopwords.txt', encoding='UTF-8').read()
stopwordSet = set(stopwords.split('\r\n'))
dictionary = corpora.Dictionary.load(project_path + 'lsi/' + 'viva.dict')
corpus = corpora.MmCorpus(project_path + 'lsi/' + 'viva.mm')
lsi = models.LsiModel.load(project_path + 'lsi/' + 'viva.lsi')
index = similarities.MatrixSimilarity.load(project_path + 'lsi/' + 'viva.index')
print('全部加载完成')

redis_conf = '211.155.92.85'
# redis_conf = '127.0.0.1'
clientReceiver = redis.Redis(host=redis_conf, port=6379, db=1)
clientSender = redis.Redis(host=redis_conf, port=6379, db=1)

receiver = clientReceiver.pubsub()

print('启动监听')

# 订阅频道
receiver.subscribe(['exactCut', 'searchCut', 'kwAnalyse', 'wordFlag', 'sentiments', 'similar']);


import jieba.posseg as pseg
def delstopwords(content):
    # words = jieba.lcut(content)
    result=''
    # for w in words:
    #     if w not in stopwords:
    #         result += w.encode('utf-8')  # +"/"+str(w.flag)+" "  #去停用词

    words = pseg.lcut(content)
    for word, flag in words:
        if (word not in stopwords and flag not in ["/x","/zg","/uj","/ul","/e","/d","/uz","/y"]): #去停用词和其他词性，比如非名词动词等
            result += word.encode('utf-8')  # +"/"+str(w.flag)+" "  #去停用词
            print result
    return result


for item in receiver.listen():

    if item['type'] == 'message':

        reqParamList = item['data'].split('!@#')

        if item['channel'] == 'exactCut':

            # 精确分词
            wordList = jieba.cut(reqParamList[1])

            clientSender.publish('cutResult', reqParamList[0] + '!@#' + ','.join(wordList))

        elif item['channel'] == 'searchCut':

            # 搜索分词
            wordList = jieba.cut_for_search(reqParamList[1])

            clientSender.publish('cutResult', reqParamList[0] + '!@#' + ','.join(wordList))

        elif item['channel'] == 'kwAnalyse':

            # 关键词提取
            wordList = jieba.analyse.extract_tags(reqParamList[1], 10, True)

            kwAnalyseResult = ''

            for aTuple in wordList:

                kwAnalyseResult += (aTuple[0] + '$%^' + str(aTuple[1]) + '$%^')

            clientSender.publish('kwAnalyseResult', reqParamList[0] + '!@#' + kwAnalyseResult)

        elif item['channel'] == 'wordFlag':

            # 词性分析
            wordList = pseg.cut(reqParamList[1])

            wordFlagResult = ''

            for words in wordList:

                wordFlagResult += words.word + '$%^' + words.flag + '$%^'

            clientSender.publish('wordFlagResult', reqParamList[0] + '!@#' + wordFlagResult)


        elif item['channel'] == 'sentiments':
            # 情感分析

            sr=pn.single_review_sentiment_score(reqParamList[1].decode('utf8'))
            print sr
            pos=sr[2]
            neg=sr[3]
            if (pos==0 and neg ==0):pos=0.5
            elif  (pos==0 and neg !=0):pos=0.1
            elif (pos!=0 and neg !=0):pos=pos/(pos+neg)
            print pos
            # sentimentsResult += words.word + '$%^' + words.flag + '$%^'

            #基于机器学习的情感分析
            s = []
            s.append(reqParamList[1].decode('utf8'))

            clf = pos_neg_ml.getPKLfile()
            pred = clf.prob_classify_many(pos_neg_ml.extract_features(s))
            pred2 = []
            for i in pred:
                pred2.append([i.prob('pos'), i.prob('neg')])
                break
            print pred2[0][0]
            clientSender.publish('sentimentsResult', reqParamList[0] + '!@#' +str(pos)+'$%^'+str(pred2[0][0]))  #pos是一般情感分析，pred2[0]是机器学习情感分析


        elif item['channel'] == 'similar':
            doc = reqParamList[1]
            doc = delstopwords(doc)
            vec_bow = dictionary.doc2bow(jieba.lcut(doc))
            vec_lsi = lsi[vec_bow]
            sims = index[vec_lsi]
            # print sims
            sort_sims = sorted(enumerate(sims), key=lambda item: -item[1])
            # sorted(word_similarities.items(), key=lambda x: x[1],reverse=True)
            no = []
            qz = []
            tempqz=[]
            ss=sort_sims[0:10]
            for i in range(len(ss)):
                if ss[i][1]>=0.99:continue  #将1：0.99相似度的文件剔除

                #取文件真实id，viva
                # files = os.listdir(docpath)
                # fileid=files[ss[i][0]]
                # fileid=fileid.split('_')
                # singleno = fileid[0]
                # singleqz = str(ss[i][1])

                #取正常文章序号
                singleno = str(ss[i][0])
                singleqz = str(ss[i][1])
                if len(qz)==0:
                    no.append(singleno)
                    qz.append(singleqz)
                    tempqz.append(singleqz)

                if abs(float(tempqz[len(tempqz)-1])-ss[i][1])>0.0015:
                    no.append(singleno)
                    qz.append(singleqz)
                tempqz.append(singleqz)

            concat = ','.join(no) + '$%^' + ','.join(qz)
            print concat
            clientSender.publish('similarResult', reqParamList[0] + '!@#' + concat)
