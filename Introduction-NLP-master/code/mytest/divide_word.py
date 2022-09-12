

def load_dictionary():
    dic = set()
    path = "D:\\my_temp_doc\\recently\\dachaung\\Introduction-NLP-master\\Introduction-NLP-master\\data\\dictionnary\\CoreNatureDictionary.mini.txt"
    for line in open(path, 'r', encoding='utf-8'):
        # print(line)
        dic.add(line[0:line.find('\t')])  # utf-8 里 tab变成了\t
        # print(dic)
    return dic

# 完全切分
def fully_segment(text, dic):
    word_list = []
    for i in range(len(text)):
        for j in range(i+1, len(text) + 1):
            word = text[i:j]
            if word in dic:
                word_list.append(word)
    return word_list

def forward_segment(text, dic):
    word_list = []
    i = 0
    while i < len(text):
        longest_word = text[i]                      # 当前扫描位置的单字
        for j in range(i + 1, len(text) + 1):       # 所有可能的结尾
            word = text[i:j]                        # 从当前位置到结尾的连续字符串
            if word in dic:                         # 在词典中
                if len(word) > len(longest_word):   # 并且更长
                    longest_word = word             # 则更优先输出
        word_list.append(longest_word)              # 输出最长词
        i += len(longest_word)                      # 正向扫描
    return word_list

dic = load_dictionary()
# print(fully_segment('就读北京大学', dic))

# print(forward_segment('就读北京大学', dic))
# print(forward_segment('研究生命起源', dic))

# 逆向最长匹配
def backward_segment(text, dic):
    word_list = []
    i = len(text) - 1
    while i >= 0:                                   # 扫描位置作为终点
        longest_word = text[i]                      # 扫描位置的单字
        for j in range(0, i):                       # 遍历[0, i]区间作为待查询词语的起点
            word = text[j: i + 1]                   # 取出[j, i]区间作为待查询单词
            if word in dic:
                if len(word) > len(longest_word):   # 越长优先级越高
                    longest_word = word
                    break
        word_list.insert(0, longest_word)           # 逆向扫描，所以越先查出的单词在位置上越靠后
        i -= len(longest_word)
    return word_list

# print(backward_segment('研究生命起源', dic))
# print(backward_segment('项目的研究', dic))

def count_single_char(word_list: list):  # 统计单字成词的个数
    return sum(1 for word in word_list if len(word) == 1)

# 双向最长匹配
def bidirectional_segment(text, dic):
    f = forward_segment(text, dic)
    b = backward_segment(text, dic)
    if len(f) < len(b):  # 词数更少优先级更高
        return f
    elif len(f) > len(b):
        return b
    else:
        if count_single_char(f) < count_single_char(b):  # 单字更少优先级更高
            return f
        else:
            return b  # 都相等时逆向匹配优先级更高


# print(bidirectional_segment('研究生命起源', dic))
# print(bidirectional_segment('项目的研究', dic))