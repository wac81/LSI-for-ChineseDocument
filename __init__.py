__author__ = 'wuanc'

import codecs
from gensim import corpora, models, similarities
from flask import Flask, request, abort,g
from .service_viva import app
project_path = './'
docpath='/home/workspace/news'
app.config['stopwords'] = codecs.open(project_path + 'stopwords.txt', encoding='UTF-8').read()
app.config['dictionary'] = corpora.Dictionary.load(project_path + 'lsi/' + 'viva.dict')
app.config['lsi'] = models.LsiModel.load(project_path + 'lsi/' + 'viva.lsi')
app.config['index'] = similarities.MatrixSimilarity.load(project_path + 'lsi/' + 'viva.index')