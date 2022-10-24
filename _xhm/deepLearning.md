b站刘二老师pytorch深度学习学习笔记

视频链接：https://www.bilibili.com/video/BV1Y7411d7Ys/?spm_id_from=333.788.recommend_more_video.-1&vd_source=1758ada68448c5de0514bddfdc10b9c9

## 1.overview

流程

```
DataSet --> model --> training --> inferring
```

## 2.线性模型

穷举法

​    重视可视化，可以通过此调整超参数

```python
import numpy as np
import matplotlib.pyplot as plt
from  mpl_toolkits.mplot3d import Axes3D 

x_data = [1.0,2.0,3.0]
y_data = [2.0,4.0,6.0]

def forward(x):
    return x*w + b

def loss(x,y):
    y_pred = forward(x)
    return (y_pred - y)*(y_pred - y)

W = np.arange(0.0,4.1,0.1)
B = np.arange(0.0,4.1,0.1)
[w,b] = np.meshgrid(W,B)

l_sum = 0
for x_val, y_val, in zip(x_data,y_data):
    y_pred_val = forward(x_val)
    loss_val = loss(x_val, y_val)
    l_sum += loss_val

fig = plt.figure()
ax = Axes3D(fig)

ax.plot_surface(w,b,l_sum/3)
ax.set_xlabel('w')
ax.set_ylabel('b')
ax.set_zlabel('loss')
plt.show()
```



## 3.梯度下降

1.分治法可能错过非凸函数的局部最优点，而且容易因为数据过大爆炸

2.梯度下降实际上使利用贪心算法

​     超参数：学习率

3.鞍点：梯度为0的点

![image-20220919172148552](https://haoming2003.oss-cn-hangzhou.aliyuncs.com/202209191721665.png)

将不再迭代更新



4.深度学习中算法选择

![image-20220919173607087](https://haoming2003.oss-cn-hangzhou.aliyuncs.com/202209191736160.png)

|      | 梯度下降 | 随机梯度下降 |
| ---- | -------- | ------------ |
| 性能 | 低       | 高           |
| 时间 | 低       | 高           |



深度学习中采用折中的办法

Mini-Batch 小批量的随机梯度下降

**梯度下降法**

```python
import matplotlib.pyplot as plt
 
# prepare the training set
x_data = [1.0, 2.0, 3.0]
y_data = [2.0, 4.0, 6.0]
 
# initial guess of weight 
w = 1.0
 
# define the model linear model y = w*x
def forward(x):
    return x*w
 
#define the cost function MSE 
def cost(xs, ys):
    cost = 0
    for x, y in zip(xs,ys):
        y_pred = forward(x)
        cost += (y_pred - y)**2
    return cost / len(xs)
 
# define the gradient function  gd
def gradient(xs,ys):
    grad = 0
    for x, y in zip(xs,ys):
        grad += 2*x*(x*w - y)
    return grad / len(xs)
 
epoch_list = []
cost_list = []
print('predict (before training)', 4, forward(4))
for epoch in range(100):
    cost_val = cost(x_data, y_data)
    grad_val = gradient(x_data, y_data)
    w-= 0.01 * grad_val  # 0.01 learning rate
    print('epoch:', epoch, 'w=', w, 'loss=', cost_val)
    epoch_list.append(epoch)
    cost_list.append(cost_val)
 
print('predict (after training)', 4, forward(4))
plt.plot(epoch_list,cost_list)
plt.ylabel('cost')
plt.xlabel('epoch')
plt.show() 
```

**随机梯度下降法**

```python
import matplotlib.pyplot as plt
 
x_data = [1.0, 2.0, 3.0]
y_data = [2.0, 4.0, 6.0]
 
w = 1.0
 
def forward(x):
    return x*w
 
# calculate loss function
def loss(x, y):
    y_pred = forward(x)
    return (y_pred - y)**2
 
# define the gradient function  sgd
def gradient(x, y):
    return 2*x*(x*w - y)
 
epoch_list = []
loss_list = []
print('predict (before training)', 4, forward(4))
for epoch in range(100):
    for x,y in zip(x_data, y_data):
        grad = gradient(x,y)
        w = w - 0.01*grad    # update weight by every grad of sample of training set
        print("\tgrad:", x, y,grad)
        l = loss(x,y)
    print("progress:",epoch,"w=",w,"loss=",l)
    epoch_list.append(epoch)
    loss_list.append(l)
 
print('predict (after training)', 4, forward(4))
plt.plot(epoch_list,loss_list)
plt.ylabel('loss')
plt.xlabel('epoch')
plt.show() 
```



## 4.反向传播backPropagation

说明：

1.Tensor中包含data和grad，data和grad也是Tensor。grad初始为None，调用l.backward()方法后w.grad为Tensor，故更新w.data时需使用w.grad.data。

> 如果w需要计算梯度，那构建的计算图中，跟w相关的tensor都默认需要计算梯度。

> 刘老师视频中a = [torch](https://so.csdn.net/so/search?q=torch&spm=1001.2101.3001.7020).Tensor([1.0]) 本文使用 a = torch.tensor([1.0])

```python
import torch
a = torch.tensor([1.0])
a.requires_grad = True # 或者 a.requires_grad_()
print(a)
print(a.data)
print(a.type())             # a的类型是tensor
print(a.data.type())        # a.data的类型是tensor
print(a.grad)
print(type(a.grad))
```

运行结果

![img](https://haoming2003.oss-cn-hangzhou.aliyuncs.com/202209241743241.png)

2.w是tensor， forward函数的返回值也是Tensor,loss函数的返回值也是Tensor

3、本算法中反向传播主要体现在，l.backward()。调用该方法后w.grad由None更新为Tensor类型，且w.grad.data的值用于后续	w.data的更新。l.backward()会把计算图中所有需要梯度(grad)的地方都会求出来，然后把梯度都存在对应的待求的参数中，最终计算图被释放。取tensor中的data是不会构建计算图的。 

```python
import torch
x_data = [1.0, 2.0, 3.0]
y_data = [2.0, 4.0, 6.0]
 
w = torch.tensor([1.0]) # w的初值为1.0
w.requires_grad = True # 需要计算梯度
 
def forward(x):
    return x*w  # w是一个Tensor

def loss(x, y):
    y_pred = forward(x)
    return (y_pred - y)**2
 
print("predict (before training)", 4, forward(4).item())

for epoch in range(100):
    for x, y in zip(x_data, y_data):
        l =loss(x,y) # l是一个张量，tensor主要是在建立计算图 forward, compute the loss
        l.backward() #  backward,compute grad for Tensor whose requires_grad set to True
        print('\tgrad:', x, y, w.grad.item())
        w.data = w.data - 0.01 * w.grad.data   # 权重更新时，注意grad也是一个tensor
 
        w.grad.data.zero_() # after update, remember set the grad to zero
 
    print('progress:', epoch, l.item()) # 取出loss使用l.item，不要直接使用l（l是tensor会构建计算图）
 
print("predict (after training)", 4, forward(4).item())
```

### 课程作业

1、手动推导线性模型y=w*x，损失函数loss=(ŷ-y)²下，当数据集x=2,y=4的时候，反向传播的过程。

答：
![在这里插入图片描述](https://haoming2003.oss-cn-hangzhou.aliyuncs.com/202209242017604.jpeg)
2、手动推导线性模型 y=w*x+b，损失函数loss=(ŷ-y)²下，当数据集x=1,y=2的时候，反向传播的过程。

答：
![在这里插入图片描述](https://haoming2003.oss-cn-hangzhou.aliyuncs.com/202209242017611.jpeg)
3、画出二次模型y=w1*x²+w2*x+b，损失函数loss=(ŷ-y)²的计算图，并且手动推导反向传播的过程，最后用[pytorch](https://so.csdn.net/so/search?q=pytorch&spm=1001.2101.3001.7020)的代码实现。

答：
构建和推导的过程
![在这里插入图片描述](https://haoming2003.oss-cn-hangzhou.aliyuncs.com/202209242017606.jpeg)

```python
import torch

x_data = [1.0,2.0,3.0]
y_data = [2.0,4.0,6.0]

w1 = torch.Tensor([1.0])#初始权值
w1.requires_grad = True#计算梯度，默认是不计算的
w2 = torch.Tensor([1.0])
w2.requires_grad = True
b = torch.Tensor([1.0])
b.requires_grad = True

def forward(x):
    return w1 * x**2 + w2 * x + b

def loss(x,y):#构建计算图
    y_pred = forward(x)
    return (y_pred-y) **2

print('Predict (befortraining)',4,forward(4))

for epoch in range(100):
    l = loss(1, 2)#为了在for循环之前定义l,以便之后的输出，无实际意义
    for x,y in zip(x_data,y_data):
        l = loss(x, y)
        l.backward()
        print('\tgrad:',x,y,w1.grad.item(),w2.grad.item(),b.grad.item())
        w1.data = w1.data - 0.01*w1.grad.data #注意这里的grad是一个tensor，所以要取他的data
        w2.data = w2.data - 0.01 * w2.grad.data
        b.data = b.data - 0.01 * b.grad.data
        w1.grad.data.zero_() #释放之前计算的梯度
        w2.grad.data.zero_()
        b.grad.data.zero_()
    print('Epoch:',epoch,l.item())

print('Predict(after training)',4,forward(4).item())
```

输出：

![image-20220924205243403](https://haoming2003.oss-cn-hangzhou.aliyuncs.com/202209242052497.png)

**总结：**
在用y=w1*x²+w2*x+b的模型训练100次后可以看到当x=4时，y=8.5，与正确值8相差比较大。原因可能是数据集本身是一次函数的数据，模型是二次函数，导致的不拟合。