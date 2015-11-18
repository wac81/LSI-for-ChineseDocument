# coding=utf-8

__author__ = 'nku'
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import re
import chardet
import os
import random
import pickle
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
import jieba.posseg as pseg
from gensim import corpora, models, similarities
from gensim.models import ldamodel
from collections import Counter


def read_file(file_loc):
    """
    读取文本文档，分词
    :param file_list: 文件的绝对路径
    :return: list, 分词的结果
    """
    flag_to_del = ["r", "m", "x", "c", "zg", "uj", "ul", "e", "d", "uz", "y", "f"]
    stop_list = [line.strip().replace("\n", "").encode() for line in open("./LDA_classes/tmp/chinese_stopword.txt", 'rb')]
    # print stop_list
    file_word = []
    p = re.compile('((http|ftp)s?://.*?(html|jpg|png|htm|jsp|txt|article).*?)')
    code_info = chardet.detect(file_loc)["encoding"]
    if not code_info:
        code_info = "utf-8"
    line = file_loc.decode(code_info, 'ignore')
    line = p.sub("", line)
    for word, flag in pseg.cut(line):
        if word not in stop_list:
            if flag not in flag_to_del and len(word) > 1:
                file_word.append(word)
    return file_word


class lda_model(object):
    def __init__(self, files, classes):
        """ doc_file is the train data dir """
        self.corpus = None
        self.tfidf_corpus = None
        self.dictionary = None
        self.lda = None
        self.index = None
        self.tfidf = None
        self.files = files
        self.classes = classes

    def set_dict_corpus(self):
        flat = lambda L: sum(map(flat, L), []) if isinstance(L, list) else [L]
        texts = [read_file(f) for f in self.files]
        # frequency = Counter(flat(texts))
        # freq_f = lambda x: x[1] > 0  # 筛选出词频大于５的词语
        # frequency = dict(filter(freq_f, frequency.items()))
        # texts = [list(set(item) & set(frequency.keys())) for item in texts]  # 更新文档删掉词频很低的词语
        # 生成字典和词袋
        self.dictionary = corpora.Dictionary(texts)  # 生成字典
        self.corpus = [self.dictionary.doc2bow(text) for text in texts]  # 生成词袋
        self.tfidf = models.TfidfModel(self.corpus)
        self.tfidf_corpus = self.tfidf[self.corpus]

    def set_lda_model(self, topic_num, chunksize=100):
        """
        加载dictionary数据和corpus词袋数据
        :param topic_num: 主题个数
        """
        self.lda = ldamodel.LdaModel(self.tfidf_corpus, id2word=self.dictionary, num_topics=topic_num, chunksize=chunksize)

    def set_index(self):
        self.index = similarities.MatrixSimilarity(self.lda[self.tfidf_corpus])

    def save_model(self, file_name):
        f = open(file_name, 'wb')
        pickle.dump(self, f)
        print("保存模型到{}".format(file_name))
        f.close()

    def save_items(self, save_doc, save_dict, save_corpus, save_lda, save_index):
        self.index.save(save_index)
        self.lda.save(save_lda, ignore=['state', 'dispatcher'])
        self.dictionary.save(save_dict)
        corpora.MmCorpus.serialize(save_corpus, self.corpus)
        file = open(save_doc, 'wb')
        pickle.dump(self.files, file)
        file.close()

    def init_from_local(self, model_file=None, dictionary_file=None, corpus_file=None, lda_file=None, doc_file=None, index_file=None):
        if model_file:
            f = open(model_file, 'rb')
            self_tmp = pickle.load(f)
            self.files = self_tmp.files
            self.corpus = self_tmp.corus
            self.dictionary = self_tmp.dictionary
            self.index = self_tmp.index
            self.tfidf_corpus = self_tmp.tfidf_corpus
            f.close()

        elif dictionary_file & corpus_file & lda_file & doc_file & index_file:
            self.dictionary = corpora.Dictionary.load(dictionary_file)
            self.corpus = corpora.MmCorpus(corpus_file)
            self.lda = ldamodel.LdaModel.load(lda_file)
            self.files = pickle.load(doc_file)
            self.index = similarities.MatrixSimilarity.load(index_file)

    def file_to_vec(self, file_loc):
        """
        新文档向量化表示
        :param file_loc: 文件的绝对路径
        :return: 分词后的文档以及向量化后的新文档
        """
        data = read_file(file_loc)
        data_vec = self.dictionary.doc2bow(data)
        new_vec = self.tfidf[data_vec]
        return data, new_vec

    def pre(self, new_vec):
        # print("the doc to pre = ", file_name)
        # file_data_sub, new_vec_tmp = self.file_to_vec(file_name)
        new_vec = self.lda[new_vec]
        sims = self.index[new_vec]
        sims = sorted(enumerate(sims), key=lambda x: x[1], reverse=True)[0]  # 提取出来最相似的文档
        # print("the near doc = ", self.files[sims[0]])
        return self.files[sims[0]], self.classes[sims[0]]

    def update(self, file_data, new_tfidf_corpus, new_files, new_classes):
        print("更新模型ing")
        self.dictionary.add_documents(file_data)  # 更新字典
        new_corpus = [self.dictionary.doc2bow(text) for text in file_data]  # 生成词袋
        self.corpus.extend(new_corpus)  # 更新词库
        self.tfidf = models.TfidfModel(self.corpus)  # 更新tf-idf模型
        self.tfidf_corpus = self.tfidf[self.corpus]
        try:
            self.lda.add_documents(new_tfidf_corpus)
        except:
            self.lda.update(new_tfidf_corpus)
        self.files.extend(new_files)
        self.set_index()
        self.classes.extend(new_classes)

if __name__ == 'ldaFindCategory':
    print "using myclass"

# if __name__ == "__main__":
#     file_path_train = "/home/acnlp/yuanhao/b/"
#     save_dict = "/home/acnlp/yuanhao/tmp/dicionary.dict"
#     save_corpus = "/home/acnlp/yuanhao/tmp/corpus.mm"
#     save_lda = "/home/nku/acnlp/yuanhao/model.lda"
#     save_index = "/home/acnlp/yuanhao/tmp/deerwester.index"
#     save_doc = "/home/acnlp/yuanhao/tmp/doc.file"
#     save_filename = "/home/acnlp/yuanhao/tmp/filename.file"
#     save_final = "/home/acnlp/yuanhao/tmp/final.file"
#
#     new_files = []  # 存储文档名
#     file_data = []  # 存储各个文档的分词结果
#     file_tfidf = []
#     topic_num = 30
#     file_path_test = "/home/nku/test_data/a/"
#
#     random.seed(1401210031)
#     files_loc = [os.path.join(root, n) for root, file, name in os.walk(file_path_train) for n in name]
#     classes = ["_".join(item.strip().split("/")[-1].split(".")[0].split("_")[:-1]) for item in files_loc]  # 训练数据的类别
#
#     files_loc_test = [os.path.join(root, n) for root, file, name in os.walk(file_path_test) for n in name]
#     files_loc_test = random.sample(files_loc_test, 20)  # 2000个测试数据
#
#     lda = lda_model(files_loc, classes)
#     lda.set_dict_corpus()
#     lda.set_lda_model(topic_num)
#     lda.set_index()
#     lda.save_items(save_dict=save_dict, save_index=save_index, save_corpus=save_corpus, save_doc=save_doc, save_lda=save_lda)
#
#     new_classes = []
#     for item in files_loc_test:
#         print('the file to predict : {}'.format(item))
#         data, data_vec = lda.file_to_vec(item)
#         out_put, out_put_class = lda.pre(data_vec)
#         print("out_put : {}".format(out_put))
#         print("out_put_class : {}".format(out_put_class), "\n")
#         new_files.append(item)
#         file_data.append(data)
#         file_tfidf.append(data_vec)
#         new_classes.append(out_put_class)
#
#     lda.update(file_data=file_data, new_files=new_files, new_tfidf_corpus=file_tfidf, new_classes=new_classes)
#     lda.save_model('/home/nku/test_data/lda.model')
#
#     model_file = open("/home/nku/test_data/lda.model", 'rb')
#     lda = pickle.load(model_file)
#     model_file.close()
#
# """
#     features = gen_svm_feature(corpus)
#     labels = []
#     for item in files_loc_1:
#         labels.append("_".join(item.split("/")[-1].split(".")[0].split("_")[:-1]))
#     mean, sd, clf = gen_svm_model(corpus, labels, features)  # corpus是一个列表
#     index_topic = find_topic(lda, topic_num, features, mean, sd, clf, labels, dictionary)
#     print("lda_topic = ")
#     k = 0
#     for i in lda.print_topics(topic_num):
#         print(index_topic[str(k)], " : ", i)
#         k += 1
#
#     num = 0
#     for i in range(50):
#         new_file = random.choice(files_loc)
#         print(new_file)
#         new_vec_tmp = file_to_vec(dictionary, new_file)
#         new_vec = tfidf[new_vec_tmp]
#         vec_lda = lda[new_vec]
#         vec_lda = sorted(vec_lda, key=lambda x: x[1], reverse=True)
#         # print(vec_lda)
#         cat0 = index_topic[str(vec_lda[0][0])]
#         if cat0 in new_file:
#             num += 1
#         pro0 = vec_lda[0][1]
#         print("The new document's category is {0}\n and the probability is {1}".format(cat0, pro0))
#     print("precision = ", num/50)
#
#     # 更新模型
#     lda.update(new_vec_tmp)
#     corpus = list(corpus)
#     corpus.append(new_vec_tmp)
#     features = gen_svm_feature(corpus)
#     labels.append(cat0)
#     mean, sd, clf = gen_svm_model(corpus, labels, features)
#     index_topic = find_topic(lda, topic_num, features, mean, sd, clf, labels, dictionary)
#     print("index_topic = ", index_topic)
#
#
#     name1 = [t.split("+") for t in lda.print_topics(topic_num)]
#     name1_0 = []
#     for item in name1:
#         sub_item = []
#         for sub_i in item:
#             sub_item.append(sub_i.split("*")[1])
#         name1_0.append("".join(sub_item))
#
#
#
#     new_file = random.choice(files_loc)
#     dictionary = corpora.Dictionary.load(save_dict)
#     corpus = corpora.MmCorpus(save_corpus)
#     new_vec = file_to_vec(dictionary, new_file)
#     vec_lda = lda[new_vec]
#     cat0 = index_topic[str(vec_lda[0][0])]
#     pro0 = vec_lda[0][1]
#     print("The new document's category is {0}\n and the probability is {1}".format(cat0, pro0))
# """
#
# """
#     files_loc_2 = random.sample(files_loc, 6000)
#     dictionary_2, corpus_2 = gen_dict_corpus(files_loc_2)
#     import time
#     print("更新模型ing")
#     t1 = time.clock()
#     lda.update(corpus_2)  # 更新LDA模型
#     name2 = [t.split("+") for t in lda.print_topics(topic_num)]
#     name2_0 = []
#     for item in name2:
#         sub_item = []
#         for sub_i in item:
#             sub_item.append(sub_i.split("*")[1])
#         name2_0.append("".join(sub_item))
#
#     index_topic = find_topic(lda, topic_num)
#     t2 = time.clock()
#     print("更新用时间{}秒".format(t2-t1))
#
#     # 对新文档进行预测
#     vec_lda = lda[new_vec]
#     cat = index_topic[str(vec_lda[0][0])]
#     pro = vec_lda[0][1]
#
#     print("对新文档进行预测以及模型的误差测量：")
#     print("The new document's category is {0}\n and the probability is {1}".format(cat0, pro0))
#     print("After update, the new document's category is {0}\n and the probability is {1}".format(cat, pro))
# #    print("#1 The LDA model's 'error' is {}.".format(lda_error1))
# #    print("#2 The LDA model's 'error' is {}.".format(lda.bound(corpus)))
#
#     out_put = set(name1_0).difference(set(name2_0))
#     print(len(out_put))
# """
