## 1.overview

流程

```
DataSet --> model --> training --> inferring
```

## 线性模型

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



## 梯度下降

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