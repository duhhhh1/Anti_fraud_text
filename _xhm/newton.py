from sympy import *
import numpy as np
from fractions import Fraction
# 定义符号
x1,x2 = symbols('x1, x2')
# 定义所求函数
r = 10
f = (x1-5)**2+(x2-3)**2-10*(x1+x2-3)**(-1)-10*(-x1+2*x2-4)**(-1)
# 求解梯度值
def get_grad(f, X):
    # 计算一阶导数
    f1 = diff(f, x1)
    f2 = diff(f, x2)
    # 代入具体数值计算
    grad = np.array([[f1.subs([(x1, X[0]), (x2, X[1])])],
                   [f2.subs([(x1, X[0]), (x2, X[1])])]])
    return grad
# 求解Hession矩阵
def get_hess(f, X):
    # 计算二次偏导
    f1 = diff(f, x1)
    f2 = diff(f, x2)
    f11 = diff(f,x1,2)
    f22 = diff(f,x2,2)
    f12 = diff(f1,x2)
    f21 = diff(f2,x1)
    # 计算具体数值计算
    hess = np.array([[f11.subs([(x1,X[0]), (x2,X[1])]),
                        f12.subs([(x1,X[0]), (x2,X[1])])],

                        [f21.subs([(x1,X[0]), (x2,X[1])]),
                        f22.subs([(x1,X[0]), (x2,X[1])])]])
    # 转换数值类型为了后续求逆矩阵
    hess = np.array(hess, dtype = 'float')
    return hess
# 牛顿迭代
def newton_iter(X0, err):
    # 记录迭代次数
    count = 0
    X1 = np.array([[0],[0]])
    while True:
        # 得到两次迭代结果差值
        X2 = X0 - X1
        if sqrt(X2[0]**2 + X2[1]**2) <= err:
            break
        else:
            hess = get_hess(f, X0)
            # 得到Hession矩阵的逆
            hess_inv = np.linalg.inv(hess)
            grad = get_grad(f, X0)
            X1 = X0 #保存上次迭代结果
            # 迭代公式
            X0 = X1 - np.dot(hess_inv, grad)
            count += 1
            print('第',count,'次迭代:','x1=',X0[0],'x2=',X0[1])
    print('迭代次数为:',count)
    print('迭代结果为',X0)
# 设置初始点
X0 = np.array([[1],[1]])
err = 1e-10
newton_iter(X0, err)

