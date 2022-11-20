---

data文件夹下是原始data和生成的data：

​	my_traindata.json是原始数据

​	stopword.list是停用词

​	label.txt是分类序号（可以不用）

​	length.txt

​	wordlabel.txt是词与数字对应关系

​	traindata和valdata是训练集和测试集，9：1

---

wordtable.py 分词（用的分字，注释部分有分词代码）并且计算词频

sen2inds.py 除停用词并且向量化

model.py 构建神经网络

textCNN.py 导入数据

train.py 训练模型

test.py 测试

---





