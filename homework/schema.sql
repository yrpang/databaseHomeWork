DROP TABLE IF EXISTS JoinStatus;
DROP TABLE IF EXISTS Association;
DROP TABLE IF EXISTS Student;
DROP TABLE IF EXISTS Class;
DROP TABLE IF EXISTS Department;
DROP TABLE IF EXISTS Dormitory;

CREATE TABLE Department(
  departNo INT PRIMARY KEY AUTO_INCREMENT,
  departName VARCHAR(20) NOT NULL,
  departOffice VARCHAR(40),
  departNum INT DEFAULT 0,
  dormitoryNo VARCHAR(20)
);

CREATE TABLE Class(
  classNo VARCHAR(10) PRIMARY KEY,
  className VARCHAR(40) NOT NULL,
  classYear SMALLINT NOT NULL,
  classNum INT DEFAULT 0,
  departNo INT NOT NULL,
  FOREIGN KEY(departNo) REFERENCES Department(departNo)
);

create TABLE Student(
  stuNo VARCHAR(11) PRIMARY KEY,
  stuName VARCHAR(20) NOT NULL,
  stuAge INT,
  classNo VARCHAR(10) NOT NULL,
  FOREIGN KEY(classNo) REFERENCES Class(classNo) ON UPDATE CASCADE
);

CREATE TABLE Association(
  societyNo INT AUTO_INCREMENT PRIMARY KEY,
  societyName VARCHAR(20) NOT NULL,
  societyYear SMALLINT,
  societyLoc VARCHAR(50)
);

CREATE TABLE JoinStatus(
  stuNo VARCHAR(11) NOT NULL,
  societyNo INT NOT NULL,
  joinYear SMALLINT NOT NULL DEFAULT 2020,
  FOREIGN KEY(stuNo) REFERENCES Student(stuNo),
  FOREIGN KEY(societyNo) REFERENCES Association(societyNo)
);

CREATE TABLE Dormitory(
  dormitoryNo VARCHAR(10) PRIMARY KEY,
  dormitoryName VARCHAR(20)
);

CREATE VIEW NAME_SOCIETY
AS
SELECT societyName Name, COUNT(*) Num
FROM Association
GROUP BY societyName;

DELIMITER $
CREATE TRIGGER UPSTUNUM
AFTER INSERT ON Student
FOR EACH ROW
BEGIN
  UPDATE Class SET classNum=classNum+1 WHERE classNo=NEW.classNo;
  UPDATE Department SET departNum=departNum+1 WHERE departNo IN (
    SELECT departNo FROM Class, Student WHERE Class.classNo=NEW.classNo
  );
END$
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
END$
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
END$
DELIMITER ;


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
END