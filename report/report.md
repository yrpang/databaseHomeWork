# 数据库大作业报告

**小组成员**：

| 姓名   | 学号        |
| ------ | ----------- |
| 庞义人 | 17130130255 |
| 陈禾嘉 | 18030400012 |
| 胡道汝 | 18030100184 |
| 唐坤   | 18030100240 |

## 1. 项目需求

​	今要建立关于系、学生、班级、学会等诸信息的一个关系数据库。一个系有若干专业，每个专业每年只招一个班，每个班有若干学生。一个系的学生住在同一宿舍区。每个学生可参加若干学会，每个学会有若干学生。学生参加某学会有一个入会年份。描述各个实体的属性（加下划线者为实体标识符）如下：

- 学生：学号、姓名、年龄、系名、班号、宿舍区。
- 班级：班号、专业名、入校年份、系名、人数。
- 系：系号、系名、系办公室地点、人数。
- 学会：学会号、学会名、成立年份、地点。

## 2. 项目构建

​	根据需求语义，我们构建的ER图如下：

![ER](..\ER.svg)

​	由上图可知，班级与学生的关系是`1:n`，学会与学生的关系是 `m:n`，而系与班级的关系是 `1:n`。 由此，我们可以确定以下的关系：

- `Student`: `stuNo`, `stuName`, `stuAge`和`classNo`
- `Society`: `societyNo`, `societyName`, `societyYear`和`societyLoc`
- `Class`: `classNo`, `className`, `classYear`和`departNo`
- `Department`: `departNo`, `departName`, `departOffice`和`dormitoryNo`

### 函数依赖分析

​	根据项目需求语义，可以得出以下FD：
$$
\begin{align}
Student: &stuNo \rightarrow stuName, 
\\&stuNo \rightarrow stuAge,
\\&stuNo \rightarrow classNo\\
Society: &societyNo \rightarrow societyName,
\\& societyNo \rightarrow societyYear, 
\\&societyNo \rightarrow societyLoc\\
Class: &classNo \rightarrow className,
\\& classNo \rightarrow departNo,
\\& classNo \rightarrow classYear,
\\& (classYear, departNo) \rightarrow classNo\\
Department:& departNo \rightarrow departName,
\\&departName \rightarrow departNo,
\\& departNo \rightarrow departOffice,
\\& departNo \rightarrow dormitoryNo
\end{align}
$$


### 模式构建

