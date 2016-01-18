# -*- coding:utf-8 -*-
from __future__ import print_function
import codecs
import time
from SentimentOne import delete_stop_words
from tgrocery import Grocery

"""
文件描述：
对新闻文字的分类
"""

##########################################
# init
model_choose = "svm"    # svm, lda, rnn
grocery_name = "./SVM_models/svm_for_news"
corpus_path = "./Corpus/NewsClassCorpus/"
file_path = "./"
file_name = "post.txt"

t_text = delete_stop_words(codecs.open(file_path + file_name, encoding='UTF-8').read())

###########################################
# 调用 SVM 模型分类
if model_choose == "svm":
    tic = time.time()
    grocery = Grocery(grocery_name)
    grocery.load()
    t_pre_result = grocery.predict(delete_stop_words(t_text))
    toc = time.time()

    t_label = t_pre_result.predicted_y
    print("Sentiment: ", t_label)
    print("How much: ", t_pre_result.dec_values[t_label])
    print("Elapsed time of predict is: %s s" % (toc-tic))
elif model_choose == "lda":
    pass
elif model_choose == "rnn":
    pass
else:
    print("")








