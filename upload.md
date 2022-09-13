在[GIthub](https://so.csdn.net/so/search?q=GIthub&spm=1001.2101.3001.7020)上Fork别人代码后，提交自己的修改，为开源贡献自己的力量。
灵活的创建分支，修改开源代码，并提交自己的修改，大致的流程分为以下几个步骤。

### 文章目录

[TOC]



## 1. Fork 别人的代码

点击Github某个代码仓库右上方的的Fork按钮，将其他人的仓库fork到自己的账号下。

## 2. 下载代码

下载自己的仓库或者下载别人的仓库都可以，如果下载别人的仓库，需要git remote add 添加自己的仓库链接，才能push到自己fork的仓库

```shell
git clone [仓库url] 
1
```

## 3. 创建自己的分支

创建自己的分支branch可以灵活的编辑、修改代码，同时不会破坏原来的master分支。

```shell
git branch [your branch]
git checkout [your branch] #切换到自己的分支 
#也可以修改本地分支的名称
git branch -m [old_name] [new_name]
1234
```

## 4. 添加自己的远程仓库地址

url表示远程仓库的地址，有两种url可以选择：
`git@github.com:facebookresearch/maskrcnn-benchmark.git` (配置好本地秘钥后可以直接push)
`https://github.com/facebookresearch/maskrcnn-benchmark.git` (每次push需要输入账号和密码)
shortname可以是远程url的名称,默认是origin,可以自己定义名称

```shell
git remote add [shortname] [url]
1
```

## 5. 修改提交

```shell
git add -u #-u表示只增加文件修改，不添加新创建的文件
git commit -m "本次提交的描述"
12
```

## 6. 推送到自己的仓库

```shell
git remote -v # 查看远程link
git push [自己的仓库url名] [分支名] #例如git push origin master 或者git push [my_repo_url] new_branch
12
```

## 7. 推送到官方仓库

```shell
#如果没有官方的url地址，需要增加上游地址，这里命名为upstream
git remote add upstream git@github.com:facebookresearch/maskrcnn-benchmark.git
# 合并官方仓库分支和本地自己修改的分支
git fetch origin
git merge origin/master
# 推送到官方仓库master分支
git push upstream master 
1234567
```

## 8. 与上游保持一致

```shell
# 获取上游更新
git fetch upstream
git checkout master
# merge
git merge upstream/master

# 推送到自己的仓库
git push origin master
```