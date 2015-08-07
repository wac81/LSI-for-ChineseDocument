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

def getIndex():
	# 加载语料
	corpus = corpora.MmCorpus( 'lsi/' + 'viva.mm')
	print 'mm loaded'

	# 加载模型
	lsi = models.LsiModel.load( 'lsi/' + 'viva.lsi')
	print 'lsi model loaded'

	# 索引
	index = similarities.MatrixSimilarity(lsi[corpus])
	index.save( 'lsi/'  + 'viva.index')
	print('index saved')
