#-*- coding: utf_8 -*-
import csv
# import json
import sys, io
import jieba
import random

# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030') #改变标准输出的默认编码

trainFile = 'data/my_traindata.json'
stopwordFile = 'data/stopword.txt'
wordLabelFile = 'data/wordLabel.txt'
trainDataVecFile = 'data/traindata_vec.txt'
valDataVecFile = 'data/valdata_vec.txt'
newTrainVecFile = 'data/new_train_vec.txt'

pad_size = 256

labelFile = 'data/label.txt'
def read_labelFile(file):
    data = open(file, 'r', encoding='utf_8').read().split('\n')
    label_w2n = {}
    label_n2w = {}
    for Line in data:
        line = Line.split(' ')
        name_w = line[0]
        name_n = int(line[1])
        label_w2n[name_w] = name_n
        label_n2w[name_n] = name_w

    return label_w2n, label_n2w


def read_stopword(file):
    data = open(file, 'r', encoding='utf_8').read().split('\n')

    return data


def get_worddict(file):
    datas = open(file, 'r', encoding='utf_8').read().split('\n')
    datas = list(filter(None, datas))
    word2ind = {}
    for line in datas:
        line = line.split(' ')
        word2ind[line[0]] = int(line[1])
    
    ind2word = {word2ind[w]:w for w in word2ind}
    return word2ind, ind2word


def csv2txt():
    label_dict, label_n2w = read_labelFile(labelFile)
    word2ind, ind2word = get_worddict(wordLabelFile)

    traindataTxt = open(trainDataVecFile, 'w')
    valdataTxt = open(valDataVecFile, 'w')
    stoplist = read_stopword(stopwordFile)
    # with open(trainFile, 'r', encoding='utf_8') as f:
    #     datas = json.load(f)
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
    # datas = list(filter(None, datas))
    # random.shuffle(datas)
    flag = 0
    for line in datas:
        # line = json.loads(line)
        title = line['简要案情']
        # cla = line['案件大类']
        # cla_ind = label_dict[cla]
        cla_ind = line["大类编号"]
        # title_seg = jieba.cut(title, cut_all=False) 分词
        title_seg = list(line['简要案情'])
        title_ind = [cla_ind]
        for w in title_seg:
            if w in stoplist:
                continue
            title_ind.append(word2ind[w])
        length = len(title_ind)
        if length > pad_size:
            title_ind = title_ind[0:pad_size]
        if length <= pad_size:
            title_ind.extend([0] * (pad_size - length))
        for n in title_ind:
            if flag%9 == 0:
                valdataTxt.write(str(n) + ',')
            else:
                traindataTxt.write(str(n) + ',')
        if flag%9 == 0:
            valdataTxt.write('\n')
        else:
            traindataTxt.write('\n')
        flag += 1

def outOrder(file1,file2):
    outOrderData = open(file2,'w')
    lines=[]
    with open(file1, 'r') as data:
        for line in data:
            lines.append(line)
        random.shuffle(lines)
        for line in lines:
            outOrderData.write(line)

def main():
    csv2txt()
    outOrder(trainDataVecFile, newTrainVecFile)

if __name__ == "__main__":
    main()