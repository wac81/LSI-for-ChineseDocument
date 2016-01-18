# -*- coding:utf-8 -*-
from __future__ import print_function

import jieba
import keras
from gensim import corpora, models, similarities
from SentimentOne import delete_stop_words


model_name = "NewsClassification"                   # 应用 keras 训练分类器模型名称
model_path = "./DeepLearn_models/" + model_name     # 应用 keras 训练分类器模型路径

file_path = "./Corpus/NewsClassCorpus/"          # 预料文件的路径



