#! /usr/bin/env python
# coding=utf-8

import codecs
import jieba
from gensim import corpora, models, similarities
from collections import defaultdict
from pprint import pprint
import sys
import os
import re
import cPickle

docpath = './news/'
lsipath = './lsi/'
# project_path = './'
# dictionary=None
dictionary=corpora.Dictionary.load(lsipath + "viva.dict")

def getFiles(docpath):
    count = 0
    files = os.listdir(docpath)
    files = sorted(files, key=lambda x: (int(re.sub('\D','',x)),x))
    arr = []

    for filename in files:
        count += 1
        print count
        arr.append(jieba.lcut(codecs.open(os.path.join(docpath ,filename)).read()))
        print filename

    return arr

def getFile(docpath):
    count = 0
    files = os.listdir(docpath)
    files = sorted(files, key=lambda x: (int(re.sub('\D','',x)),x))
    for filename in files:
        count += 1
        print count
        try:
            yield codecs.open(docpath + filename).read()
        except:
            print(docpath)
            continue
        print filename




# from multiprocessing.dummy import Pool as ThreadPool

# def deal_corpora(str):
#     # print str
#     # print jieba.lcut(str)
#     return dictionary.doc2bow(jieba.lcut(str))

# def MyCorpus():
# 	pool=ThreadPool(4)
# 	dic = pool.map(deal_corpora,  getFile())
# 	# print 'kkkkkkkkkkkkk'
# 	pool.close()
# 	pool.join()

# class MyCorpus(object):
#     def __iter__(self):
#     	pool=ThreadPool(4)
# 		dic = pool.map(deal_corpora,  getFile())
# 		# print 'kkkkkkkkkkkkk'
# 		pool.close()
# 		pool.join()



# 语料库 docpath 为文件存储位置
def getCorpus(docpath='./news/'):
    # 加载字典
    # dictionary=corpora.Dictionary.load('lsi/' + 'viva.dict')
    # dictionary = dict
    print 'Dict loaded'
    docpath = docpath
    corpus = MyCorpus()
    corpora.MmCorpus.serialize(lsipath + 'viva.mm', corpus)
    corpus_list = [dictionary.doc2bow(jieba.lcut(file)) for file in getFile(docpath)]
    fp = open(lsipath + "viva_cor_list.list", 'w')
    cPickle.dump(corpus_list, fp)
    print('Corpus Saved')
    return  corpus


class MyCorpus(object):
    def __iter__(self):
        # dictionary = pool.map(dictionary.doc2bow,  getFile())
        for file in getFile(docpath):
            yield dictionary.doc2bow(document=jieba.lcut(file))
