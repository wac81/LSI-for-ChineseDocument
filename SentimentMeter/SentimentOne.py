# -*- coding:utf-8 -*-
from __future__ import print_function
from tgrocery import Grocery
import xlrd
import sys
import json
import jieba
import os


########################################################
# functions
def sentiment_train(gro_name, train_set):
    """

    :param gro_name:
    :param train_set:
    :return:
    """
    gro_ins = Grocery(gro_name)
    # gro_ins.load()
    gro_ins.train(train_set)
    print("Is trained? ", gro_ins.get_load_status())
    gro_ins.save()


def get_xls_train_set(files, num_text):
    """
    Get train set from excel(.xls)
    :param files: List of file names.
    :param num_text: Texts line read each train.
    :return:    List of tuple [(label, text), (_, _),(,)]
    """
    train_set = []
    for t_file in files:
        data = xlrd.open_workbook(t_file)
        table = data.sheet_by_index(0)
        num_line = min(table.nrows, num_text)
        print("Read %s lines from %s." % (num_line, t_file))
        for t_line in range(num_line):
            train_set.append((t_file.split("/")[-1].split(".")[0], table.cell(t_line, 0).value.encode('utf-8')))
    return train_set


def get_txt_train_set(files, num_text):
    """
    Get train set from text(.txt)
    :param files: List of file names.
    :param num_text: Texts line read each train.
    :return:    List of tuple [(label, text), (_, _),(,)]
    """
    import re
    train_set = []
    count_line = 1
    for t_file in files:
        if t_file.split('.')[-1] != "txt":
            raise "****** Wrong file type during train set, a .txt file excepted ******"
        fp = open(t_file, 'rb')
        contents = fp.readlines()
        fp.close()
        for t_content in contents:
            if count_line > num_text:
                break
            pattern = re.search(r'([0-9]+)(\s+)(.*)', t_content)
            if pattern:
                t_label = pattern.group(1)
                t_text = pattern.group(3)
            else:
                print("ERROR: re wrong in line_%s: %s" % (count_line, t_content))
                break
            train_set.append((t_label, t_text))
            count_line += 1
    return train_set


def delete_stop_words(str_in):
    """
    去停用词
    :param str_in:  string
    :return:    string
    """
    import codecs
    path_stop_words = "./"
    file_stop_words = "chinese_stopword.txt"

    t_list = list(jieba.cut(str_in))
    if os.path.isfile(path_stop_words + file_stop_words):
        stop_words = codecs.open(path_stop_words + file_stop_words, encoding='UTF-8').read()
    else:
        print("No stop words given.")
        stop_words = []

    t_content_a = ""
    for i in t_list:
        if i in stop_words:
            continue
        else:
            t_content_a += i.encode('utf-8')
    return t_content_a


def get_class_txt_train_set(file_path_in, files):
    """
    从带分类的文本文件中取语料，取自LDA程序。
    :param files: List of file names.
    :param file_path_in:
    :return:    List of tuple [(label, text), (_, _),(,)]
    """
    import re
    train_set = []
    for t_file in files:
        t_label = re.search(r'(.*)(_)(.*)$', t_file).group(1)
        t_content = open(file_path_in + t_file, 'rb').read()
        t_content = delete_stop_words(t_content)
        print("Read contents from %s." % t_file)
        train_set.append((t_label, t_content))
    return train_set


def get_scores(predicts):
    """

    :param predicts:  Class of Geometric Margin.
    :return:
    """
    scores = {}
    index = (max(predicts.dec_values))


def json_dict_from_file(json_file):
    """
    load json file and generate a new object instance whose __name__ filed
    will be 'inst'
    """
    obj_s = []
    with open(json_file) as f:
        for line in f:
            object_dict = json.loads(line, encoding='utf-8')
            obj_s.append(object_dict)
    return obj_s


#####################################################################
# predict

def predict_for_json(grocery_in, json_file, to_json_file):
    """

    :param json_file:
    :return:
    """
    tag_name = "autoTags"
    fout = open(to_json_file, 'ab')
    json_list = json_dict_from_file(json_file)
    for json_dict in json_list:
        json_dict_temp = json_dict
        content = json_dict['content']
        t_pre_result = grocery_in.predict(content)
        t_label = t_pre_result.predicted_y
        json_dict_temp[tag_name] = t_label
        fout.write((json.dumps(json_dict_temp) + '\r\n').encode('utf-8'))
        print("Write complete!")


def predict_for_one(grocery_in):
    """
    Predict label for one sentents you enter.
    :param grocery_in:  Grocery instance.
    :return:    print in stdout.
    """
    while 1:
        print("Enter the sentence you want to test(\"quit\" to break): ", end='\b')
        t_text = sys.stdin.readline()
        if "quit" in t_text:
            break
        t_pre_result = grocery_in.predict(t_text)
        t_label = t_pre_result.predicted_y
        # if max(pre_result.dec_values) < 0.03:
        #     label = "neutral"
        print("Sentiment: ", t_label)
        print("How much: ", max(t_pre_result.dec_values))


########################################################
# main
if __name__ == "__main__":
    import time
    grocery_name = "./meter"
    corpus_path = "./Corpus/"
    max_line_num_once = 1000000  # 每个文件中读取的最大行数

    tic = time.time()
    file_list = [
        corpus_path + "neg.xls",
        corpus_path + "pos.xls"
    ]
    train_src = get_xls_train_set(file_list, max_line_num_once)

    sentiment_train(grocery_name, train_src)
    toc = time.time()
    print("Elapsed time of training is: ", toc - tic)

    grocery = Grocery(grocery_name)
    grocery.load()

    predict_for_one(grocery)



