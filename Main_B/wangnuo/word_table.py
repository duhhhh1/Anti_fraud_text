# -*- coding: utf-8 -*-
'''
将训练数据使用jieba分词工具进行分词。并且剔除stopList中的词。
得到词表：
        词表的每一行的内容为：词 词的序号 词的频次
'''

import csv
# import json
import jieba
from tqdm import tqdm

trainFile = 'data/my_traindata.json'
stopwordFile = 'data/stopword.txt'
wordLabelFile = 'data/wordLabel.txt'
lengthFile = 'data/length.txt'


def read_stopword(file):
    data = open(file, 'r', encoding='utf_8').read().split('\n')

    return data


def main():
    worddict = {}
    stoplist = read_stopword(stopwordFile)
    # with open(trainFile, 'r', encoding='utf_8') as f:
    #     datas = json.load(f)
    # datas = list(filter(None, datas))
    datas = []
    with open('data/datas.txt','r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',')
        fieldnames = next(reader)
        reader = csv.DictReader(f, fieldnames=fieldnames, delimiter=',')
        for row in reader:
            new_dict={}
            new_dict['大类编号'] = row['大类编号']
            new_dict['简要案情'] = row['简要案情']
            datas.append(new_dict)

    data_num = len(datas)
    len_dic = {}
    for line in datas:
        # 分词
        # title = line['简要案情']
        # title_seg = jieba.cut(title, cut_all=False)   
         
        # 分字
        title_seg = list(line['简要案情'])
        length = 0
        for w in title_seg:
            if w in stoplist:
                continue
            length += 1
            if w in worddict:
                worddict[w] += 1
            else:
                worddict[w] = 1
        if length in len_dic:
            len_dic[length] += 1
        else:
            len_dic[length] = 1

    wordlist = sorted(worddict.items(), key=lambda item:item[1], reverse=True)
    f = open(wordLabelFile, 'w', encoding='utf_8')
    ind = 0
    for t in wordlist:
        d = t[0] + ' ' + str(ind) + ' ' + str(t[1]) + '\n'
        ind += 1
        f.write(d)

    for k, v in len_dic.items():
        len_dic[k] = round(v * 1.0 / data_num, 3)
    len_list = sorted(len_dic.items(), key=lambda item:item[0], reverse=True)
    f = open(lengthFile, 'w')
    for t in len_list:
        d = str(t[0]) + ' ' + str(t[1]) + '\n'
        f.write(d)

if __name__ == "__main__":
    main()

