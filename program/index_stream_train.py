#! /usr/bin/env python
# coding=utf-8

import codecs
import jieba
from gensim import corpora, models, similarities
from collections import defaultdict
from pprint import pprint
import sys
import os

# project_path = './'
# lsipath = './lsi/'
def getIndex(lsipath):
	# 加载语料
	corpus = corpora.MmCorpus( lsipath + 'viva.mm')
	print 'mm loaded'

	# 加载模型
	lsi = models.LsiModel.load( lsipath + 'viva.lsi')
	print 'lsi model loaded'

	# 索引
	index = similarities.MatrixSimilarity(lsi[corpus])
	index.save( lsipath  + 'viva.index')
	print('index saved')
