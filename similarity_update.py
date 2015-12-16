# coding=utf-8
import codecs
import jieba
from gensim import corpora, models, similarities
from gensim.models import lsimodel
import jieba.posseg as pseg
import codecs
stopwords = codecs.open('stopwords.txt', encoding='UTF-8').read()
import os
import re
import sys
import cPickle
import time
import itertools
sys.path.append("./program/")

# constants #######################################################
lsipath = './lsi/'
docpath = './news/'     # text posted one by one, otherwise docpath="./news_add/"
DECAY_FACTOR = 1.0      # decay factor[0.0, 1.0] for merging two decomposed matrix
text = "阿斯顿马丁拉贡达汽车之友2015月刊曾经辉煌英国老牌豪华品牌命运挺坎坷阿斯顿马丁例外坚持顶级手工制造面对竞争对手不断技术进步必须要出招酝酿几年LagondaTaraf车型终于面世土豪新宠看到熟悉马丁车型朋友觉得有点陌生难道家族脸产生其实LagondaTaraf借鉴搭载V8发动机Lagonda轿车设计元素后者1976发布上市WilliamTowns设计Lagonda名称一款量产车上得到回归阿斯顿马丁意义非凡说明擅长超跑品牌未来偏向实用性顶级车型出现1976LagondaSeriesII上市采用很多先进技术包括液晶仪表盘闻名先辈款阿斯顿马丁LagondaTaraf利用很多现代化创新设计车身采用碳纤维材料修长车身四门四座设计内部营造空间内饰风格一成不变精致手工内饰绝对不忍心坐上去称为精致轿跑车新车基于阿斯顿马丁VH平台打造搭载V12发动机LagondaTaraf限量投产台最大功率404kW最大扭矩约619NmRapideS车型使用发动机相同传动部分可能采用采埃孚速自动变速箱动力系统乏善可陈该车阿斯顿特殊项目部设计作品部门最近推出VulcanVantageGT3车型一台Lagonda阿斯顿马丁Gaydon工厂手工打造工厂之前专门打造One77超跑车新款阿斯顿马丁Lagonda跟随定制项目推出包括售价万英镑阿斯顿马丁CC100SpeedsterCC100Speedster量产版阿斯顿马丁定制部门打造阿斯顿马丁官方宣布已经发售中东地区LagondaTaraf面向法国德国英国俄罗斯中国香港24国家地区进行销售中国大陆北美地区没有列入本次增加销售名单当中当然外国土豪买买提供受邀请消费者购买价格不菲Lagonda历史拉贡达Lagonda创始人WilburGunn附近一条小河名字1906公司英格兰成立1947阿斯顿马丁公司收购成为子公司1974陆续投产三款车型过于超前外形极其昂贵售价鲜有问津世纪90年代没有新车阿斯顿马丁拉贡达汽车之友2015月刊曾经辉煌英国老牌豪华品牌命运挺坎坷阿斯顿马丁例外坚持顶级手工制造面对竞争对手不断技术进步必须要出招酝酿几年LagondaTaraf车型终于面世土豪新宠看到熟悉马丁车型朋友觉得有点陌生难道家族脸产生其实LagondaTaraf借鉴搭载V8发动机Lagonda轿车设计元素后者1976发布上市WilliamTowns设计Lagonda名称一款量产车上得到回归阿斯顿马丁意义非凡说明擅长超跑品牌未来偏向实用性顶级车型出现1976LagondaSeriesII上市采用很多先进技术包括液晶仪表盘闻名先辈款阿斯顿马丁LagondaTaraf利用很多现代化创新设计车身采用碳纤维材料修长车身四门四座设计内部营造空间内饰风格一成不变精致手工内饰绝对不忍心坐上去称为精致轿跑车新车基于阿斯顿马丁VH平台打造搭载V12发动机LagondaTaraf限量投产台最大功率404kW最大扭矩约619NmRapideS车型使用发动机相同传动部分可能采用采埃孚速自动变速箱动力系统乏善可陈该车阿斯顿特殊项目部设计作品部门最近推出VulcanVantageGT3车型一台Lagonda阿斯顿马丁Gaydon工厂手工打造工厂之前专门打造One77超跑车新款阿斯顿马丁Lagonda跟随定制项目推出包括售价万英镑阿斯顿马丁CC100SpeedsterCC100Speedster量产版阿斯顿马丁定制部门打造阿斯顿马丁官方宣布已经发售中东地区LagondaTaraf面向法国德国英国俄罗斯中国香港24国家地区进行销售中国大陆北美地区没有列入本次增加销售名单当中当然外国土豪买买提供受邀请消费者购买价格不菲Lagonda历史拉贡达Lagonda创始人WilburGunn附近一条小河名字1906公司英格兰成立1947阿斯顿马丁公司收购成为子公司1974陆续投产三款车型过于超前外形极其昂贵售价鲜有问津世纪90年代没有新车阿斯顿马丁拉贡达汽车之友2015月刊曾经辉煌英国老牌豪华品牌命运挺坎坷阿斯顿马丁例外坚持顶级手工制造面对竞争对手不断技术进步必须要出招酝酿几年LagondaTaraf车型终于面世土豪新宠看到熟悉马丁车型朋友觉得有点陌生难道家族脸产生其实LagondaTaraf借鉴搭载V8发动机Lagonda轿车设计元素后者1976发布上市WilliamTowns设计Lagonda名称一款量产车上得到回归阿斯顿马丁意义非凡说明擅长超跑品牌未来偏向实用性顶级车型出现1976LagondaSeriesII上市采用很多先进技术包括液晶仪表盘闻名先辈款阿斯顿马丁LagondaTaraf利用很多现代化创新设计车身采用碳纤维材料修长车身四门四座设计内部营造空间内饰风格一成不变精致手工内饰绝对不忍心坐上去称为精致轿跑车新车基于阿斯顿马丁VH平台打造搭载V12发动机LagondaTaraf限量投产台最大功率404kW最大扭矩约619NmRapideS车型使用发动机相同传动部分可能采用采埃孚速自动变速箱动力系统乏善可陈该车阿斯顿特殊项目部设计作品部门最近推出VulcanVantageGT3车型一台Lagonda阿斯顿马丁Gaydon工厂手工打造工厂之前专门打造One77超跑车新款阿斯顿马丁Lagonda跟随定制项目推出包括售价万英镑阿斯顿马丁CC100SpeedsterCC100Speedster量产版阿斯顿马丁定制部门打造阿斯顿马丁官方宣布已经发售中东地区LagondaTaraf面向法国德国英国俄罗斯中国香港24国家地区进行销售中国大陆北美地区没有列入本次增加销售名单当中当然外国土豪买买提供受邀请消费者购买价格不菲Lagonda历史拉贡达Lagonda创始人WilburGunn附近一条小河名字1906公司英格兰成立1947阿斯顿马丁公司收购成为子公司1974陆续投产三款车型过于超前外形极其昂贵售价鲜有问津世纪90年代没有新车阿斯顿马丁拉贡达汽车之友2015月刊曾经辉煌英国老牌豪华品牌命运挺坎坷阿斯顿马丁例外坚持顶级手工制造面对竞争对手不断技术进步必须要出招酝酿几年LagondaTaraf车型终于面世土豪新宠看到熟悉马丁车型朋友觉得有点陌生难道家族脸产生其实LagondaTaraf借鉴搭载V8发动机Lagonda轿车设计元素后者1976发布上市WilliamTowns设计Lagonda名称一款量产车上得到回归阿斯顿马丁意义非凡说明擅长超跑品牌未来偏向实用性顶级车型出现1976LagondaSeriesII上市采用很多先进技术包括液晶仪表盘闻名先辈款阿斯顿马丁LagondaTaraf利用很多现代化创新设计车身采用碳纤维材料修长车身四门四座设计内部营造空间内饰风格一成不变精致手工内饰绝对不忍心坐上去称为精致轿跑车新车基于阿斯顿马丁VH平台打造搭载V12发动机LagondaTaraf限量投产台最大功率404kW最大扭矩约619NmRapideS车型使用发动机相同传动部分可能采用采埃孚速自动变速箱动力系统乏善可陈该车阿斯顿特殊项目部设计作品部门最近推出VulcanVantageGT3车型一台Lagonda阿斯顿马丁Gaydon工厂手工打造工厂之前专门打造One77超跑车新款阿斯顿马丁Lagonda跟随定制项目推出包括售价万英镑阿斯顿马丁CC100SpeedsterCC100Speedster量产版阿斯顿马丁定制部门打造阿斯顿马丁官方宣布已经发售中东地区LagondaTaraf面向法国德国英国俄罗斯中国香港24国家地区进行销售中国大陆北美地区没有列入本次增加销售名单当中当然外国土豪买买提供受邀请消费者购买价格不菲Lagonda历史拉贡达Lagonda创始人WilburGunn附近一条小河名字1906公司英格兰成立1947阿斯顿马丁公司收购成为子公司1974陆续投产三款车型过于超前外形极其昂贵售价鲜有问津世纪90年代没有新车"
name = "3044336629515138_阿斯顿·马丁 拉贡达"
####################################################################


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
            # print result
    return result

def getFile(docpath):
    count = 0
    files = os.listdir(docpath)
    files = sorted(files, key=lambda x: (int(re.sub('\D','',x)),x))
    for filename in files:
        count += 1
        print count
        try:
            yield codecs.open(os.path.join(docpath ,filename)).read()
        except:
            continue
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


# Extended Dictionary #################################################################
t1 = time.time()
text = delstopwords(text)
text_vec = jieba.lcut(text.decode('unicode-escape'))
dict1 = corpora.Dictionary.load(lsipath + 'viva.dict')
corpus = corpora.MmCorpus(lsipath +'viva.mm')
dict1.add_documents([text_vec])
dict1.save(lsipath + 'viva.dict')
t2 = time.time()
dictionary = dict1

print "Elapsed time of Extended Dictionary is: ", t2-t1, "s"


# Updated Corpus ########################################################################
corpus = []
fp = open(lsipath + "viva_cor_list.list", 'r')
corpus = cPickle.load(fp)
fp.close()

corpus_add = [dictionary.doc2bow(text_vec)]
if (corpus_add[0] in corpus):
    pass
else:
    fp_f = open(unicode(docpath + name, 'utf8'), 'w')
    fp_f.write(text)
    fp_f.close()
    corpus.append(corpus_add[0])

# corpus = [dictionary.doc2bow(jieba.lcut(file)) for file in getFile(docpath)]

fp = open(lsipath + "viva_cor_list.list", 'w')
cPickle.dump(corpus, fp)
fp.close()


# Updated LSI Model ####################################################################
t1 = time.time()
lsi = lsimodel.LsiModel(corpus, id2word=dictionary, num_topics=300,chunksize=20000)
lsi.save( lsipath  + 'viva.lsi')
t2 = time.time()
print "Elapsed time of Updated LSI Model is: ", t2-t1, "s"


# Updated LSI Index #######################################################################
t1 = time.time()
tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]
lsi_vec = lsi[corpus]
index = similarities.MatrixSimilarity(lsi_vec)
index.save( lsipath  + 'viva.index')
print('index saved')
t2 = time.time()
print "Elapsed time of Updated LSI Index is: ", t2-t1, "s"

from flask import Flask, request, abort,g,current_app
app = Flask(__name__)
project_path = './'
app.config['dictionary'] = corpora.Dictionary.load(project_path + 'lsi/' + 'viva.dict')
app.config['lsi'] = models.LsiModel.load(project_path + 'lsi/' + 'viva.lsi')
app.config['index'] = similarities.MatrixSimilarity.load(project_path + 'lsi/' + 'viva.index')
print('load')