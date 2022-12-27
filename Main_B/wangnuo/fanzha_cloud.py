import jieba  # 分词
from matplotlib import pyplot as plt  # 绘图，数据可视化
from wordcloud import WordCloud  # 词云
from PIL import Image  # 图片处理
import numpy as np  # 矩阵运算
import pandas as pd

data = pd.read_csv('wangnuo/data/datas.csv')
print(len(data))

texts = ""
for idx in range(4332):
    texts = texts + data['简要案情'][idx]

cut = jieba.cut(texts)
string = ' '.join(cut)
wordlist = string.split(' ')
stopwords = open('wangnuo/data/stopword.txt', 'r', encoding='utf_8').read().split('\n')
wordlist2 = [word for word in wordlist if not word in stopwords]


wordset = set(wordlist2)

counts={}
for key in wordset:
     counts[key] = wordlist2.count(key)
#获取前10个元素的个数变为列表
tens = sorted(counts.values(),reverse=True)[0:120]
print(tens)
#统计最终前十的元素及出现次数
tendict = {}
for k in counts.keys():
    if counts[k] in tens:
        tendict.setdefault(counts[k],k.strip("\n"))
print(tendict)
wordlist3 = tendict.values()

string = ' '.join(wordlist3)

img = Image.open('wangnuo/tree.jpg')  # 打开遮罩图片
print(img)
img_array = np.array(img)
wc = WordCloud(
    background_color='white',
    mask=img_array,
    font_path="msyh.ttc"  # 字体所在位置：C:\Window\Fonts
)
wc.generate_from_text(string)

# 绘制图片
fig = plt.figure(1)
plt.imshow(wc)
plt.axis('off')  # 不显示坐标轴

# plt.show()显示生成的词云图片

plt.savefig('wangnuo/word.jpg', dpi=1000)