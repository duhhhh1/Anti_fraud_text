**python学习笔记**

1.print  语句

​			a  = 10

​           b = "asc"

​			print（“我的命只是%d” %a)  中间没有逗号

  			print ("数值%d 字符串%s"%(a,b))

​			print("asd""sd""sd",sep=".")   sep="."以 .  为分隔符，没有默认为空格

   		print("Sda",end="")				end = 什么都没有下个输出紧跟，\t一个tab， \n换行。

 2.条件语句

 1）  注意格式  if 条件 :(英文冒号)

​							   执行语句（注意缩进）

​                     	  elif  条件:

​								执行语句

​						   else:
​								执行语句

2）嵌套时 同样缩进来判断语句

   if   条件:

​		if 	条件:

​             	执行语句

​		else：

​				执行语句

​	else：

   	执行语句

3. 生成随机数

   1）import   random  (引入随即库)

   ​	x = random.randint(a,b)  (随机生成a,b内的一个整数)

4.循环结构

​		1）for格式 for i in range（5）:  从0到4整数输出                    注意  ：

​                 for i in range(0,10,3) :  从0到9间隔3输出,大于9后不会输出

 				for i in range(-10,-100,-30):  负向输出

​				name 是字符串时     for i  in  name:    按%c输出每个字符

​	2）	while格式  while 条件: 

​									执行语句

​		    while 与 else 联合用

​							while 条件:

​									执行语句

​							else：  不满足while条件时执行一次

​									执行语句

5.字符串

1) '''              ''' 注释

2）“”“      ”“” 表示段落，输出原内容一模一样

3)"       " 中单引号可以直接输出        ‘           ’ 里的双引号可以直接输出

  ‘       ’ 中的单引号可以通过\ ‘  来打印，同理双引号里的双引号可以通过\输出

4）str 是字符串时   str[a:b]可以截取  str[a:d:c] 按c间隔截取、

​			str[a:] 直接读到末尾

​           str[:a]从头读到a

5) print（str + “你好") 打印str内容直接更上你好-----字符串连接使用

​     print（str * 3) 打印三次str

  print(r"hello \n chengdu")  前面有r 内部的\失效，会打印出来

6.列表

1）列表内可以储存不同类型的元素

2）列表是写在[]里的 ，中间用逗号隔开   如list = [123，3214]

3）索引值以0为开始值，-1为末尾的开始值

4）可以使用+来连接两个列表，*表示重复

5）遍历时 可以 for i in list:  来从前向后遍历，i会自动向后取值

6）增

   将一个元素加入列表  list.append（），若加的是一个列表，会将列表看成一个元素加入，会保留列表的[]

​	 将两个列表合并成一个列表，list.extend()。

  将一个元素插入到列表指定下标位置  list.insert（a,b）,将元素a插入到列表b的位置

   7）删

  将指定下标位置的元素删除   del list[a]  

  将列表最后一个元素弹出 list.pop()

  移除指定内容的元素 list.remove(a)    将列表中第一个a删除

8）改

通过下标直接修改 list[a] =     

9)查（在不在） in or not in

 if  a （not） in list：

​        执行语句

else：

   	执行语句

10）list.index(a,b,c)  在列表中下标为b，到c-1中寻找是否有a，并返回是b到c-1中的第几个

list.count(a) 统计列表中有几个a

list.reverse()将列表中所有元素反转

list.sort()将列表升序排

list.sort(reverse = True) 降序

若列表中的元素还是列表，可以通过二维数组的方式访问



7.元组

1）元组的元素不能修改，写在小括号里，用逗号隔开  例如t = (“asd”，123)

2）但可以包含变量

3）tup=(50)不是元组，但tup=(50,)是元组（只有一个数据）

4）可以通过下标直接访问，-1是末尾，可以切片（左闭右开）

5）增

连接两个元组tup = tup1 + tup2（实际上是创建了一个新的元组，把两者放入）

6）删

可以直接把元组直接删去，不能删除某一指定元素





8.字典

1）储存键值对，同一个字典中键必须是唯一的

2）建立时 如info = {"name": "乌鸦嘴","age":18}

​	访问时 print(info["name"])

​	访问不存在的键时，直接访问会报错，若写print(info.get("gender"))，没有会返回None

3）增

info["id"] = Newid

新增建赋予他值

4）删

 del info["name"]  删除了指定键值对后，再次访问键会出错

del info 删除字典后，访问会出错

info.clear()  清空字典

5）修改

info["name"] = 

6)查

info.keys()  得到所有的键

info.values() 得到所有的值

info.items() 得到所有的键值对

for key,value in info.items():

​    print("key = %s,value = %s"%(key,value))

若想对列表进行这样的操作可以通过枚举函数enumerate（list）

for i，x in enumerate（list）

   print（i，x）



9.函数

1）定义  def 函数名（）

​			  执行语句

2）调用时  函数名（）

3）带参数的函数 def add2Num(a,b):

​									c = a+b

 									print(c)

add2Num(11,22)

4)带返回值的函数

​		def  add2Num(a,b):

​			return a+b;

print(add2Num(11,22))

5)返回多个值的函数

  def divid(a,b):

   	shang = a/b

​		yushu = a%b

 	return shang,yushu

sh,yu = divid(5,2)       需要多个值来保存返回值

6）函数中局部变量优先（若全局变量的名字与局部变量的名字相同）

7）若函数中加入 global a 会改变全局变量



10.文件操作

1）文件打开  f  = open("test.txt","w") 

2）文件关闭 f.close()

3）f.read(num) 读取num个字符，开始时定位在文件头部，每执行一次向后移动num个字符

4）f.readlines() 将文件每行作为一个字符串以一个列表元素储存，可进行列表的操作

  f.readline()每次只能读取文件的一行，执行后移动到下一行

11 异常处理

1）异常捕获

  try:

​       执行内容

except （错误1，错误2，……）一个可以不用括号：（IOError：输入输出错误，NameError：命名错误）若上面的执行内容错误类型符合这个错误则执行下面语句。

​    执行内容

2）获取错误描述

  try:

​       执行内容

except （错误1，错误2，……）as result：

​    执行内容

   print（result）  错误信息获取

 3）捕获所有异常

except Exception as result：（Exception 可以承接所有异常）

4）

try：

​     执行内容

except Exception as result：

​    执行内容

finally:（无论是否有异常都会执行）常用于打开文件失败时要关闭文件

​     执行内容

