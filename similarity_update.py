# coding=utf-8
import codecs
import jieba
from gensim import corpora, models, similarities
import jieba.posseg as pseg
import codecs
stopwords = codecs.open('stopwords.txt', encoding='UTF-8').read()
import os
import re
import sys
sys.path.append("./program/")
lsipath = './lsi/'
docpath = './news_added'
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

def getFile(docpath):
    count = 0
    files = os.listdir(docpath)
    files = sorted(files, key=lambda x: (int(re.sub('\D','',x)),x))
    for filename in files:
        count += 1
        print count
        yield codecs.open(os.path.join(docpath ,filename)).read()
        print filename

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


if  os.path.exists(docpath):
    from ar import filebyfileHandleSingleProcess
    filebyfileHandleSingleProcess(docpath,100)   #100字符内的文件抛掉不处理,多进程默认 multiprocess=4
# dictionary = corpora.Dictionary(texts)

# for file in getFile(docpath):
#     yield dictionary.doc2bow(jieba.lcut(file))
dictionary = corpora.Dictionary(jieba.lcut(file) for file in getFile(docpath))
corpus = [dictionary.doc2bow(jieba.lcut(file)) for file in getFile(docpath)]
# corpus = corpora.MmCorpus(lsipath +'viva.mm')
# corpus.add_documents()
dictionary.add_documents(getFiles(docpath))
tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]
lsi = models.LsiModel.load(lsipath + 'viva.lsi')
print 'lsi model loaded'
lsi.add_documents(corpus)

print 'lsi model update'
index = similarities.MatrixSimilarity.load(lsipath + 'viva.index')
index.add_documents(corpus)
# index = similarities.MatrixSimilarity(lsi)
# lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=400)