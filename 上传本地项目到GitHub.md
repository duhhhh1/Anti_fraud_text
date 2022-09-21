# 上传本地项目到GitHub

## 1.准备工作

#### （1）.创建ssh

安装git之后，创建一个文件夹，在打开文件夹之后，在任意地方右击，选择Git Bash Here，进入Git客户端窗口。

 ![image-20220921213417312](C:\Users\86185\AppData\Roaming\Typora\typora-user-images\image-20220921213417312.png)

输入 (ssh-keygen -t rsa -C "1903605737@qq.com")  邮箱为创建github时的邮箱，回车，会在用户目录中生成一个.ssh文件夹，

![image-20220921214022268](C:\Users\86185\AppData\Roaming\Typora\typora-user-images\image-20220921214022268.png)

此时回到GitHub进行设置，点击个人头像，打开Settings -> 选择SSH and GPG keys -> 选择New SSH key -> 设置一个tittle ->将之前生成的.ssh文件夹中的id_rsa.pub文件用文本查看器打开，复制里面的内容，粘贴到Github该页面的Key中。

（成功后邮箱会收到邮件）

#### （2）.查看ssh是否创建成功

在Git客户端窗口中输入 （ssh -T git@github.com)

输入yes后看到如下后。则表示成功连到GitHub

![image-20220921214815786](C:\Users\86185\AppData\Roaming\Typora\typora-user-images\image-20220921214815786.png)

## 2.上传代码

#### 1.输入命令"git init",初始化git，此时就会在文件夹目录下生成一个".git"的文件夹。

#### 2.回到git命令窗口，输入命令“git add ."这是上传所有文件，（命令"git add  文件名"是上传特定的文件）

`git add *   //添加所有文件到暂存区`

`git add .    //添加所有文件到暂存区`

`git add -u .  // -u 表示将**已跟踪文件中的修改和删除的文件**添加到暂存区，不包括新增加的文件`

`git add -A     //-A 表示将所有的已跟踪的文件的修改与删除和新增的未跟踪的文件都添加到暂存区`

`git add *.html  //添加某种文件类型 `

`git add *.txt   //添加某种文件类型`

`git add try/     //添加文件夹到,如try文件夹` 

#### 3.输入"git commit -m ……"将项目提交到github中.

#### 4.在GitHub中创建一个新仓库 ,新建仓库后,复制仓库地址

![image-20220921225439012](C:\Users\86185\AppData\Roaming\Typora\typora-user-images\image-20220921225439012.png)

#### 5.输入命令 "git remote add origin 刚刚复制的网址"

#### 6.输入命令"git push -u origin master"输入用户名与密码就完成了项目的上传