# coding=utf8

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import json
import codecs
import jieba
# import jieba.analyse
import jieba.posseg as pseg
# import redis
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
from gensim import corpora, models, similarities
from flask import Flask, request, abort
app = Flask(__name__)

project_path = './'
docpath='/home/workspace/news'

@app.route('/similar/<input_text>',methods=['GET', 'POST'])
def similar(input_text):
    re=object
    if request.method == 'POST':
        re = request.form['text']
    else:
        try:
            re = input_text  # 获取GET参数，没有参数就赋值 0
        except ValueError:
            abort(404)      # 返回 404
    result = json.dumps(similar_search(re))
    print result
    return result


@app.route('/')
def index():
    return '相似度推荐 for viva，GET方式：请访问/similar/[传入字串] \n POST方式：请访问/similar/post  post体里text=[传入字串]'

def similar_search(request):
    doc = request
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
        files = os.listdir('./news/')
        fileid=files[ss[i][0]]
        fileid=fileid.split('_')
        singleno = fileid[0]
        singleqz = str(ss[i][1])

        #取正常文章序号
        # singleno = str(ss[i][0])
        # singleqz = str(ss[i][1])

        if len(qz)==0:
            no.append(singleno)
            qz.append(singleqz)
            tempqz.append(singleqz)

        if abs(float(tempqz[len(tempqz)-1])-ss[i][1])>0.0015:
            no.append(singleno)
            qz.append(singleqz)
        tempqz.append(singleqz)

    # concat = ','.join(no) + '$%^' + ','.join(qz)
    concat = {'similarNO':no,'similarQZ':qz}
    # concat = []
    # concat.append(no)
    # concat.append(qz)
        # {no,qz}
    # print concat
    return concat
        # clientSender.publish('similarResult', reqParamList[0] + '!@#' + concat)


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

if __name__ == '__main__':
    stopwords = codecs.open(project_path + 'stopwords.txt', encoding='UTF-8').read()
    # stopwordSet = set(stopwords.split('\r\n'))
    dictionary = corpora.Dictionary.load(project_path + 'lsi/' + 'viva.dict')
    corpus = corpora.MmCorpus(project_path + 'lsi/' + 'viva.mm')
    lsi = models.LsiModel.load(project_path + 'lsi/' + 'viva.lsi')
    index = similarities.MatrixSimilarity.load(project_path + 'lsi/' + 'viva.index')
    print('All loaded')
    app.run(debug=True,  port=3000)


