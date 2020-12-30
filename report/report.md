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

### 2.1 函数依赖分析

​	根据项目需求语义，我们可以确定以下的关系：

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

![ER](..\ER.svg)

​	其中，班级与学生的关系是`1:n`，学会与学生的关系是 `m:n`，而系与班级的关系是 `1:n`。 

### 2.2 系统实现

#### 2.2.1 建表
实现于文件`schema.sql`
~~~mysql
CREATE TABLE Department(
  departNo INT PRIMARY KEY AUTO_INCREMENT,
  departName VARCHAR(20) NOT NULL,
  departOffice VARCHAR(40),
  departNum INT DEFAULT 0,
  dormitoryNo VARCHAR(20)
);
~~~
一些介绍
~~~mysql
CREATE TABLE Class(
  classNo VARCHAR(10) PRIMARY KEY,
  className VARCHAR(40) NOT NULL,
  classYear SMALLINT NOT NULL,
  classNum INT DEFAULT 0,
  departNo INT NOT NULL,
  FOREIGN KEY(departNo) REFERENCES Department(departNo)
);
~~~
一些介绍
~~~mysql
create TABLE Student(
  stuNo VARCHAR(11) PRIMARY KEY,
  stuName VARCHAR(20) NOT NULL,
  stuAge INT,
  classNo VARCHAR(10) NOT NULL,
  FOREIGN KEY(classNo) REFERENCES Class(classNo) ON UPDATE CASCADE
);
~~~
一些介绍
~~~mysql
CREATE TABLE Association(
  societyNo INT AUTO_INCREMENT PRIMARY KEY,
  societyName VARCHAR(20) NOT NULL,
  societyYear SMALLINT,
  societyLoc VARCHAR(50)
);
~~~
一些介绍
~~~mysql
CREATE TABLE JoinStatus(
  stuNo VARCHAR(11) NOT NULL,
  societyNo INT NOT NULL,
  joinYear SMALLINT NOT NULL DEFAULT 2020,
  FOREIGN KEY(stuNo) REFERENCES Student(stuNo),
  FOREIGN KEY(societyNo) REFERENCES Association(societyNo)
);
~~~
一些介绍
~~~mysql
CREATE TABLE Dormitory(
  dormitoryNo VARCHAR(10) PRIMARY KEY,
  dormitoryName VARCHAR(20)
);
~~~
一些介绍
~~~mysql
CREATE OR REPLACE VIEW NAME_SOCIETY AS
(
  SELECT Association.societyNo, Association.societyName Name, COUNT(DISTINCT Student.stuNo) Num
  FROM Association LEFT OUTER JOIN JoinStatus ON(Association.societyNo=JoinStatus.societyNo) LEFT OUTER JOIN Student ON(JoinStatus.stuNo=Student.stuNo)
  GROUP BY societyNo
);

~~~
一些介绍
~~~mysql
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
~~~

#### 2.2.2 建立学会视图

~~~mysql
create view ...
~~~

#### 2.2.3 触发器实现

~~~mysql
-- 在此处插入触发器的代码
~~~



还有一些我没有想到的功能就都放在这里。

```

```

jjkljkl

* jklj
* 客户客户开具、


- 看
- 解开了解开了


ljkhnjk


### 2.3 前端-后端接口

~~~javascript
# 不知道该写什么，留给义人8，LOL
# 最好再配一张图（需要的话告诉我）
# Hejia
~~~



## 3. 设计总结

