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
  classNum INT,
  departNo INT NOT NULL,
  FOREIGN KEY(departNo) REFERENCES Department(departNo)
);

create TABLE Student(
  stuNo VARCHAR(11) PRIMARY KEY,
  stuName VARCHAR(20) NOT NULL,
  stuAge INT,
  classNo VARCHAR(10) NOT NULL,
  FOREIGN KEY(classNo) REFERENCES Class(classNo)
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
  joinYear SMALLINT NOT NULL,
  FOREIGN KEY(stuNo) REFERENCES Student(stuNo),
  FOREIGN KEY(societyNo) REFERENCES Association(societyNo)
);

CREATE TABLE Dormitory(
  dormitoryNo VARCHAR(10) PRIMARY KEY,
  dormitoryName VARCHAR(20)
);

