# -*- coding:utf-8 -*-
from __future__ import print_function
import time
import os
from tgrocery import Grocery
from SentimentOne import sentiment_train, predict_for_one, predict_for_json, get_class_txt_train_set


"""
文件说明：
用 SVM 模型来对新闻进行分类，训练模型的过程
预料存储在/home/baobao/Projects/Lavector/SentimentMeter/Corpus/ClassCorpusFromLDA
模型存储在/home/baobao/Projects/Lavector/SentimentMeter/SVM_models/classification_from_LDA
"""

##########################################
# init
grocery_name = "./SVM_models/svm_for_news"
corpus_path = "./Corpus/NewsClassCorpus/"

##########################################
# train svm
tic = time.time()
file_list = os.listdir(corpus_path)
train_src = get_class_txt_train_set(corpus_path, file_list)
sentiment_train(grocery_name, train_src)
toc = time.time()
print("Elapsed time of training is: ", toc - tic)

###########################################
# process
grocery = Grocery(grocery_name)
grocery.load()

file_path = "./"
file_name = "post.txt"

predict_for_one(grocery)
# predict_for_json(grocery, file_path + file_name, file_path + to_file_name)

