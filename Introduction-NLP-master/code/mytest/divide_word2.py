from pyhanlp import *


# def load_dictionary():
#     dic = set()
#     path = "D:\\my_temp_doc\\recently\\dachaung\\Introduction-NLP-master\\Introduction-NLP-master\\data\\dictionnary\\CoreNatureDictionary.mini.txt"
#     for line in open(path, 'r', encoding='utf-8'):
#         # print(line)
#         dic.add(line[0:line.find('\t')])  # utf-8 里 tab变成了\t
#         # print(dic)
#     return dic

# 不显示词性
HanLP.Config.ShowTermNature = False

# 可传入自定义字典 [dir1, dir2]
segment = DoubleArrayTrieSegment()
# 激活数字和英文识别
segment.enablePartOfSpeechTagging(True)
#
# print(segment.seg("江西鄱阳湖干枯，中国最大淡水湖变成大草原"))
# print(segment.seg("上海市虹口区大连西路550号SISU"))

def load_from_file(path):
    """
    从词典文件加载DoubleArrayTrie
    :param path: 词典路径
    :return: 双数组trie树
    """
    map = JClass('java.util.TreeMap')()  # 创建TreeMap实例
    with open(path, 'r', encoding='utf-8') as src:
        for word in src:
            word = word.strip()  # 去掉Python读入的\n
            map[word] = word
    return JClass('com.hankcs.hanlp.collection.trie.DoubleArrayTrie')(map)


## 去掉停用词
def remove_stopwords_termlist(termlist, trie):
    return [term.word for term in termlist if not trie.containsKey(term.word)]


trie = load_from_file('D:\\my_temp_doc\\recently\dachaung\\Introduction-NLP-master\\Introduction-NLP-master\\data\\dictionnary\\stopwords.txt')
termlist = segment.seg("江西鄱阳湖干枯了，中国最大的淡水湖变成了大草原")
print('去掉停用词前：', termlist)

print('去掉停用词后：', remove_stopwords_termlist(termlist, trie))
