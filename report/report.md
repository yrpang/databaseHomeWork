# 数据库大作业报告

**小组成员**：

|  姓名  |    学号     |
| :----: | :---------: |
| 庞义人 | 17130130255 |
| 陈禾嘉 | 18030400012 |
| 胡道汝 | 18030100184 |
|  唐坤  | 18030100240 |

## 1. 任务要求

今要建立关于系、学生、班级、学会等诸信息的一个关系数据库。一个系有若干专业，每个专业每年只招一个班，每个班有若干学生。一个系的学生住在同一宿舍区。每个学生可参加若干学会，每个学会有若干学生。学生参加某学会有一个入会年份。描述各个实体的属性（加下划线者为实体标识符）如下：

- 学生：学号、姓名、年龄、系名、班号、宿舍区。
- 班级：班号、专业名、入校年份、系名、人数。
- 系：系号、系名、系办公室地点、人数。
- 学会：学会号、学会名、成立年份、地点。

## 2. 整体架构设计

系统整体定位为一个web项目，整体架构如下图1所示，前端采用微信小程序，后端使用 `flask` 框架，数据库选用 `MySQL5.7` ，为方便本地练习及线上系统使用，数据库使用腾讯云的云MySQL。

<center>
 <img style="padding:10px; background-color:#fff; " src="..\ER.svg">
 <br>
 <div style="display: inline-block; color: #000; padding: 2px;">图1</div> 
</center>

## 2. 数据库设计

### 2.1 函数依赖分析

根据项目需求语义，我们可以确定以下的关系：

- `Student`: `stuNo`, `stuName`, `stuAge`和`classNo`
- `Society`: `societyNo`, `societyName`, `societyYear`和`societyLoc`
- `Class`: `classNo`, `className`, `classYear`和`departNo`
- `Department`: `departNo`, `departName`, `departOffice`和`dormitoryNo`

可以得出以下FD：
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

根据分析，我们构建的ER图如下：

<center>
	<img style="padding:10px; background-color:#fff; " src="..\ER.svg">
	<br>
	<div style="display: inline-block; color: #000; padding: 2px;">图2</div> 
</center>

其中，班级与学生的关系是`1:n`，学会与学生的关系是 `m:n`，而系与班级的关系是 `1:n`。 

### 2.2 系统实现

#### 2.2.1 建表

##### 2.2.1.1 Department表

```SQL
CREATE TABLE Department(
  departNo INT PRIMARY KEY AUTO_INCREMENT,
  departName VARCHAR(20) NOT NULL,
  departOffice VARCHAR(40),
  departNum INT DEFAULT 0,
  dormitoryNo VARCHAR(20)
);
```

##### 2.2.1.2 Class表

```SQL
CREATE TABLE Class(
  classNo VARCHAR(10) PRIMARY KEY,
  className VARCHAR(40) NOT NULL,
  classYear SMALLINT NOT NULL,
  classNum INT DEFAULT 0,
  departNo INT NOT NULL,
  FOREIGN KEY(departNo) REFERENCES Department(departNo)
);
```

##### 2.2.1.3 Student表

```SQL
create TABLE Student(
  stuNo VARCHAR(11) PRIMARY KEY,
  stuName VARCHAR(20) NOT NULL,
  stuAge INT,
  classNo VARCHAR(10) NOT NULL,
  FOREIGN KEY(classNo) REFERENCES Class(classNo) ON UPDATE CASCADE
);
```

##### 2.2.1.4 Association表

```SQL
CREATE TABLE Association(
  societyNo INT AUTO_INCREMENT PRIMARY KEY,
  societyName VARCHAR(20) NOT NULL,
  societyYear SMALLINT,
  societyLoc VARCHAR(50)
);
```

##### 2.2.1.5 JoinStatus表

```SQL
CREATE TABLE JoinStatus(
  stuNo VARCHAR(11) NOT NULL,
  societyNo INT NOT NULL,
  joinYear SMALLINT NOT NULL DEFAULT 2020,
  FOREIGN KEY(stuNo) REFERENCES Student(stuNo),
  FOREIGN KEY(societyNo) REFERENCES Association(societyNo)
);
```

##### 2.2.1.6 Domitory表

```SQL
CREATE TABLE Dormitory(
  dormitoryNo VARCHAR(10) PRIMARY KEY,
  dormitoryName VARCHAR(20)
);
```

#### 2.2.2 建立学会视图

此视图展示学会的学会名以及学生数量

```SQL
CREATE OR REPLACE VIEW NAME_SOCIETY AS
(
  SELECT Association.societyNo, Association.societyName Name, COUNT(DISTINCT Student.stuNo) Num
  FROM Association LEFT OUTER JOIN JoinStatus ON(Association.societyNo=JoinStatus.societyNo) LEFT OUTER JOIN Student ON(JoinStatus.stuNo=Student.stuNo)
  GROUP BY societyNo
);
```

#### 2.2.3 触发器实现

根据每个班的学生变动情况自动增减班级表和系表的人数字段的值，以完成要求的后端设计要求。
##### 2.2.3.1 增加学生数量触发器

```SQL
DELIMITER $
CREATE TRIGGER UPSTUNUM
AFTER INSERT ON Student
FOR EACH ROW
BEGIN
  UPDATE Class SET classNum=classNum+1 WHERE classNo=NEW.classNo;
  UPDATE Department SET departNum=departNum+1 WHERE departNo IN (
    SELECT departNo FROM Class, Student WHERE Class.classNo=NEW.classNo
  );
END;
$
DELIMITER ;
```

##### 2.2.3.2 减少学生数量触发器

```SQL
DELIMITER $
CREATE TRIGGER DECSTUNUM
AFTER DELETE ON Student
FOR EACH ROW
BEGIN
  UPDATE Class SET classNum=classNum-1 WHERE classNo=OLD.classNo;
  UPDATE Department SET departNum=departNum-1 WHERE departNo IN (
    SELECT departNo FROM Class, Student WHERE Class.classNo=OLD.classNo
  );
END;
$
DELIMITER ;
```

##### 2.2.3.3 更新学生数量触发器

```SQL
DELIMITER $
CREATE TRIGGER UPDATESTUNUM
AFTER UPDATE ON Student
FOR EACH ROW
BEGIN
  UPDATE Class SET classNum=classNum+1 WHERE classNo=NEW.classNo;
  UPDATE Department SET departNum=departNum+1 WHERE departNo IN (
    SELECT departNo FROM Class, Student WHERE Class.classNo=NEW.classNo
  );
  UPDATE Class SET classNum=classNum-1 WHERE classNo=OLD.classNo;
  UPDATE Department SET departNum=departNum-1 WHERE departNo IN (
    SELECT departNo FROM Class, Student WHERE Class.classNo=OLD.classNo
  );
END;
$
DELIMITER ;
```

#### 2.2.3 建立函数

给定一个班的旧班号和新班号，把所有相关表中此班的旧班号改为新班号，并返回此班的人数，以完成后端设计要求。

```SQL
DELIMITER $
CREATE FUNCTION change_classNo(old_classNo VARCHAR(20), new_classNo VARCHAR(20))
RETURNS INT
BEGIN
  DECLARE num INT DEFAULT 0;

  UPDATE Class
  SET classNo=new_classNo
  WHERE classNo=old_classNo;

  UPDATE Student
  SET classNo=new_classNo
  WHERE classNo=old_classNo;

  SELECT COUNT(*) INTO num
  FROM Student
  WHERE classNo=new_classNo;

  RETURN(num);
END;
$
DELIMITER ;
```

#### 2.2.4 建立存储过程

使用游标完成如下功能：确定系表中人数字段的值与实际学生数是否相符。如果不相符，把人数字段的值改为实际数，并返回此系的系号、系名、原人数、实际人数。

```SQL
DELIMITER $
CREATE PROCEDURE FIXNUM()
BEGIN
  DECLARE done INT DEFAULT FALSE;
  DECLARE id, num, real_num INT;
  DECLARE tmp_name VARCHAR(20);
  DECLARE cur CURSOR FOR SELECT departNo, departName, departNum FROM Department;
  DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

  OPEN cur;

  DROP TABLE IF EXISTS tmp_table;
  CREATE TEMPORARY TABLE tmp_table
  (
    departNo INT NOT NULL,
    departName VARCHAR(20),
    old_num INT NOT NULL,
    new_num INT NOT NULL
  );

  deal_loop: LOOP
    FETCH cur INTO id, tmp_name, num;

    IF done THEN
      LEAVE deal_loop;
    END IF;

    SELECT COUNT(*) INTO real_num
    FROM Student, Class, Department
    WHERE Student.classNo=Class.classNo AND Class.departNo=Department.departNo AND Department.departNo=id;

    IF real_num!=num THEN
      UPDATE Department
      SET departNum=real_num
      WHERE departNo=id;

      INSERT INTO tmp_table
      VALUES(id, tmp_name, num, real_num);
    END IF;
  END LOOP;

  CLOSE cur;
END;
$
DELIMITER ;
```

### 2.3 前端-后端接口

```javascript
# 不知道该写什么，留给义人8，LOL
# 最好再配一张图（需要的话告诉我）
# Hejia
```

## 3. 设计总结

在本次上机实验中，我们小组完成了学生管理系统的设计，其中前端部分使用微信小程序实现，后端部分选用 flask 框架，数据库选择的是MySQL。在前期准备过程中，我们首先进行了项目分析，明确需要做的工作，然后把项目放在了GitHub上，进行完成。因为组长有过微信小程序的开发经验，所以前端部分是比较顺利的。在后端项目开发中，我们先大致从整体上学习了有关数据库的知识，一些不懂的问题通过查找资料获得了很好地解决。首先画出ER图，然后将ER图转化为关系模型，然后，再设计各个实体及属性。具体设计部分，将数据库部分任务下分到每个小组成员，大家交流完成后，再整合到一起。最后，完成了全部的工作之后，我们对项目进行了测试，在测试过程中我们还发现了一些问题，于是大家在群里进行了充分的讨论，最后进行解决。经过多次修改，项目最终完成。在本次学生管理系统的设计中，相比知识本身，我觉得更重要的是解决问题的能力，以及团队合作开发项目的能力。经过此次上机实验，我们小组团队学到了很多，对数据库理论有了更深入地了解，相信对以后的学习和工作会有很大的帮助！
