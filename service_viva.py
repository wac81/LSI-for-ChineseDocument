# coding=utf8

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import json
import codecs
import jieba
jieba.initialize()   #manual initialize jieba

# import jieba.analyse
import jieba.posseg as pseg
# import redis
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
from gensim import corpora, models, similarities
from flask import Flask, request, abort,g,current_app
# from werkzeug.contrib.fixers import ProxyFix
app = Flask(__name__)

project_path = './'
docpath='/home/workspace/news'

# @app.before_first_request
# @app.before_request
def appd():
    app.config['stopwords'] = codecs.open(project_path + 'stopwords.txt', encoding='UTF-8').read()
    app.config['dictionary'] = corpora.Dictionary.load(project_path + 'lsi/' + 'viva.dict')
    app.config['lsi'] = models.LsiModel.load(project_path + 'lsi/' + 'viva.lsi')
    app.config['index'] = similarities.MatrixSimilarity.load(project_path + 'lsi/' + 'viva.index')
    print('All loaded')
appd()

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
    vec_bow = app.config['dictionary'].doc2bow(jieba.lcut(doc))
    vec_lsi = app.config['lsi'][vec_bow]
    sims = app.config['index'][vec_lsi]
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
        # print ss[i]
        # print ss[i][0]
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

    concat = {'similarNO':no,'similarQZ':qz}
    return concat


def delstopwords(content):
    result=''

    words = jieba.lcut(content)
    for w in words:
        if w not in app.config['stopwords']:
            result += w.encode('utf-8')  # +"/"+str(w.flag)+" "  #去停用词

    # words = pseg.lcut(content)
    # with app.test_request_context():
    # for word, flag in words:
    #     if (word not in app.config['stopwords'] and flag not in ["/x","/zg","/uj","/ul","/e","/d","/uz","/y"]): #去停用词和其他词性，比如非名词动词等
    #         result += word.encode('utf-8')  # +"/"+str(w.flag)+" "  #去停用词
    #             print result
    return result



if __name__ == '__main__':
    with app.app_context():
        print current_app.name
    app.run(debug=False, host='0.0.0.0', port=3000)


