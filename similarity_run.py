# coding=utf-8
import jieba
from gensim import corpora, models, similarities
from multiprocessing import Pool





import os
import sys
import shutil
sys.path.append("./program/")
# def f(x):
    # return corpora.Dictionary(jieba.lcut('我们可以'))

if __name__ == '__main__':
	filesaved = 'article.sql'
	docpath='./news/'
	lsipath='./lsi/'
	if os.path.exists(docpath):
		shutil.rmtree(docpath)  #删除目录
	if os.path.exists(lsipath):
		shutil.rmtree(lsipath)  #删除目录

	if  not os.path.exists(docpath):
		from ar import spiltDocument
		spiltDocument(filesaved,docpath,100,100)   #最多分割100个文件，100字符内的文件抛掉不处理

	from dict_stream_train import getDictionary
	dict=getDictionary()

	from corpus_stream_train import getCorpus
	corpus=getCorpus()

	from lsi_stream_train import getLsiModel
	lsimodel=getLsiModel()

	from index_stream_train import getIndex
	getIndex()
    # p = Pool(5)
    # d = corpora.Dictionary(jieba.cut('我们可以'))
    # print d
    # print( corpora.Dictionary(jieba.lcut('我们可以')))
    # print(p.map(f, ['aa', 'ab', 'ac']))