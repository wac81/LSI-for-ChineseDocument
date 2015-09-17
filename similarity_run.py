# coding=utf-8
import os
import sys
# import shutil
import time
sys.path.append("./program/")
# def f(x):
    # return corpora.Dictionary(jieba.lcut('我们可以'))
time_before = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
print time_before

import jieba.posseg as pseg
import codecs
stopwords = codecs.open('stopwords.txt', encoding='UTF-8').read()
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

# doc = delstopwords('你们觉得天地会的人真心把他当自己人仅仅是因为他滑头？康熙把他当最珍贵的【划去】基【/划去】朋友仅仅是因为他胆子大？')
# print doc
if __name__ == '__main__':
	filesaved = 'article.sql'
	docpath='./nnews/'
	lsipath='./nlsi/'
	# if os.path.exists(docpath):
	# 	shutil.rmtree(docpath)  #删除目录
	# if os.path.exists(lsipath):
	# 	shutil.rmtree(lsipath)  #删除目录

	if  os.path.exists(docpath):
		from ar import filebyfileHandle
		filebyfileHandle(docpath,100,4)   #100字符内的文件抛掉不处理,多进程默认 multiprocess=4

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

timenow = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
print time_before
print timenow