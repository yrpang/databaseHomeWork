## 1. 项目架构及任务综述

### 架构
emmm因为我不懂其它的东西，所以项目定位为一个web项目，前端部分使用`微信小程序`实现，后端部分选用 `flask` 框架，数据库选择 `mysql`。

### 任务

前端小程序、后端整体框架由 @yrpang 完成，数据库设计大家一同完成，具体功能实现在[4-任务分工](#4-任务分工)部分认领自己的开发任务分工完成，`clone` 本仓库在自己的电脑完成自己负责部分的开发，手工进行充分测试后，`commit`并直接`push`到本仓库。

因为项目人数非常少，并且对大家完全充分信任，所以仓库给每个人完全访问权限，不需要提交 `Pull Request` ，直接 `push` 即可，请大家在操作前简单了解 `git` 的基本使用方法，另外出于安全考虑**禁止**使用 `--force` 选项，如果遇到无法解决的问题请联系我，不要 `--force` ！！！

### 整体deadline

因为分工后每个人的工作量相对不大，所以项目第一版定在`12.10(周四) 上机验收前`完成，当天有上机安排，我们可以见面一起讨论做一些细节上的优化，然后完成验收。

每个人的任务deadline见[4-任务分工](#4-任务分工)

请在deadline之前完成自己任务的开发和测试以及代码提交，我们争取上机直接验收然后就可以去浪啦hhh～

## 2. 关于数据库

### 配置情况简述

1. 使用 `mysql 5.7`
2. 为了避免重复在本地配置数据库的麻烦提升我们的协作效率，使用云数据库，项目中的连接我已经配置好。
3. 使用的数据库名称为`homework`，生产和测试环境直接使用同一个，此处偷懒，大家不要删库跑路（逃。

### 数据库信息

|  项目  | 值                             |
| :----: | :----------------------------- |
| 用户名 | root                           |
|  密码  | database2020__                 |
|  地址  | cdb-n3duly12.bj.tencentcdb.com |
|  端口  | 10065                          |

### 连接方法

如果使用 `mysql` 自带的命令行管理工具的话请输入
```bash
mysql -h cdb-n3duly12.bj.tencentcdb.com -u root -P 10065 -p
```

密码输入 `database2020__` 。

之后就和本地完全一样了。


## 3. 项目开发流程及关键性DDL

整体流程分为三个部分:

- 完成后端框架的搭建、上线工作; 负责人: @yrpang DDL: `(12月5日 周六 23:59)`
- 微信小程序开发; 负责人: @yrpang DDL: 待定，根据接口协调情况确定
- 数据库整体方案设计; 负责人: <全体> 定稿DDL: `(12月6日 周日 23:59)`
- 按照下面[任务分工](#4-任务分工)完成各功能api的实现
- 第一版完成; DDL: `(12月10日 周四 18:00)`

注: 上面时间均为北京时间(UTC/GMT+08:00)

## 4. 任务分工

**API接口暂定如下，随着个人开发进度可以根据需要进行调整，请大家认领任务，把自己的名字写在后面，push到项目里，同时就当作熟悉git的使用了。**

### 总体返回值约定

适用于下面的所有API，前端会判断如果`errCode`不为0会弹出说明给用户发生了什么错误。

正常返回: {'errCode':0, 'status':'OK', 'data':{如果有就返回，没有则忽略这一个}}

异常返回: {'errCode': -1, 'status':'具体错误信息'}

### 班级管理（陈禾嘉）

- `/class/add` POST {'data': {'classNo': 'string', 'className': 'string', 'classYear':'int', 'departNo': 'int', 'classNum': 'int'}}
- `/class/edit` POST 
- `/class/del` POST {'data': {'classNo' 'string'}} **级连删除**
- `/class/get/all` GET 返回值{'errCode':0, 'status':'OK', 'data': [...班级基本信息列表]}
- `/class/get/<classNo>` GET 返回值{'errCode':0, 'status':'OK', 'data': [...班级具体信息列表]}



### 系管理

- `/depart/add` POST {'data': {'departNo': 'string', 'departName': 'string', 'departOffice': 'string', 'departNum': 'int', 'dormitoryNo': 'string'}}
- `/depart/edit` POST 
- `/depart/del` POST {'data': {'departNo' 'string'}} **级连删除**
- `/depart/get/all` GET 返回值{'errCode':0, 'status':'OK', 'data': [...系基本信息列表]}
- `/depart/get/<departNo>` GET 返回值{'errCode':0, 'status':'OK', 'data': [...系具体信息列表]}


### 学会管理

- `/society/add` POST {'data': {'societyNo': 'string', 'societyName': 'string', 'societyYear':'int', 'societyLoc': 'string'}}
- `/society/edit` POST 
- `/society/del` POST {'data': {'societyNo' 'string'}} **级连删除**
- `/society/get/all` GET 返回值{'errCode':0, 'status':'OK', 'data': [...学会基本信息列表]}
- `/society/get/<societyNo>` GET 返回值{'errCode':0, 'status':'OK', 'data': [...学会具体信息列表]}


### 宿舍区管理

- `/dormitory/add` POST {'data': {'dormitoryNo': 'string', 'dormitoryName': 'string'}}
- `/dormitory/edit` POST 
- `/dormitory/del` POST {'data': {'dormitoryNo' 'string'}} **级连删除**
- `/dormitory/get/all` GET 返回值{'errCode':0, 'status':'OK', 'data': [...宿舍区基本信息列表]}
- `/dormitory/get/<dormitoryNo>` GET 返回值{'errCode':0, 'status':'OK', 'data': [...宿舍区具体信息列表]}

### 学生管理

- `/student/add` POST {'data': {'stuNo': 'string', 'stuName': 'string', 'stuAge': 'int', 'departNo': 'string', 'classNo': 'string'}}
- `/student/edit` POST 
- `/student/del` POST {'data': {'dormitoryNo' 'string'}} **级连删除**
- `/student/get/all` GET 返回值{'errCode':0, 'status':'OK', 'data': [...宿舍区基本信息列表]}
- `/student/get/<dormitoryNo>` GET 返回值{'errCode':0, 'status':'OK', 'data': [...宿舍区具体信息列表]}

## 5. 基本指南

1. `git clone https://github.com/yrpang/databaseHomeWork.git`
2. 进入项目文件夹
3. `pip install -r requirements.txt` 如果有报错进行相应处理
4. 验证环境配置 `python3 run.py`，之后打开`http://127.0.0.1:5000`，显示成功即为配置完成
5. 打开`homework/api.py`进行相应开发，只需要关心这一个文件，其它可以不用管
