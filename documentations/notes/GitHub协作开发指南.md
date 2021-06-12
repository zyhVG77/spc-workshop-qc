# 1 准备工作

首先，克隆仓库的develop分支到本地

```bash
# 进入你想放置项目的文件夹
git clone -b develop https://github.com/zyhVG77/SpcApp.git
```

然后创建自己的feature分支

```bash
# 进入项目根目录
git flow feature start [your feature name]
# 分支名推荐格式：
# 1. 前端开发的feature: frontend-你名字的缩写
# 2. 后端开发的feature: backend-你名字的缩写
# 3. 恢复历史代码的feature: restore-history
# 4. 其他feature: 自己DIY
```

# 2 前端开发

进入前端目录，先用npm安装依赖的node包，然后运行调试用服务器

```bash
# 进入frontend/目录下
npm install
npm run serve
```

由于前端的数据返回依赖后端，所以要么在mock里模拟数据返回，要么进入后端文件夹运行后端的服务器：

```bash
# 进入backend/
python manage.py runserver
```

# 3 后端开发

略

# 4 提交feature

先同步到远端仓库

```bash
git add [files your wanna push]
git commit -m 'comment'
git push
```

然后有两种方法将其合并到develop分支。

第一，直接merge

```bash
# 用传统方法先检出再合并
git checkout develop
git merge feature_branch

# 或用flow一步完成，结束当前feature
git flow feature finish feature_branch
```

更新远端

```bash
git push
```

第二，发起**pull request**

进入github主页，发起一个**pull request**申请将本feature分支并入develop分支。这样大家都能看到你的修改。

# 5 参考

1. [Gitflow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow#:~:text=The%20overall%20flow%20of%20Gitflow,merged%20into%20the%20develop%20branch)