#! /usr/bin/env python
# coding=utf-8

import codecs
import jieba
from gensim import corpora, models, similarities
from collections import defaultdict
from pprint import pprint
import sys
import os

docpath = './a/'
# project_path = './'
# dictionary=None
dictionary=corpora.Dictionary.load('lsi/' + 'viva.dict')

def getFile(docpath):
    count = 0
    for filename in os.listdir(docpath.decode('utf-8')):
        count += 1
        print count
        yield codecs.open(docpath + filename).read()




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



# 语料库
def getCorpus(docpath='./a/'):
    # 加载字典
    # dictionary=corpora.Dictionary.load('lsi/' + 'viva.dict')
    # dictionary = dict
    print 'Dict loaded'
    docpath=docpath
    corpus = MyCorpus()
    corpora.MmCorpus.serialize('./lsi/' + 'viva.mm', corpus)
    print('Corpus Saved')
    return  corpus


class MyCorpus(object):
    def __iter__(self):
		# dictionary = pool.map(dictionary.doc2bow,  getFile())
        for file in getFile(docpath):
            yield dictionary.doc2bow(jieba.lcut(file))
