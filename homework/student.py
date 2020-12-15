from logging import exception
from flask_restful import Resource, reqparse, abort
from homework.db import get_db
import datetime
from mysql.connector.errors import Error

# 下面为student的api的实现(Hejia Chen)
parser_studentItem = reqparse.RequestParser()
parser_studentItem.add_argument(
    'stuName', required=True, type=str, help="stuName not provide.")
parser_studentItem.add_argument(
    'stuAge', type=int, help="stuAge not provide.")
parser_studentItem.add_argument(
    'classNo', required=True, type=str, help="classNo not provide.")


class studentItem(Resource):
    def checkIfExist(self, stuNo):  # 查询是否存在
        cur = get_db().cur

        cur.execute("SELECT * FROM Student WHERE stuNo='%s'" % stuNo)
        if(len(cur.fetchall()) < 1):
            return False
        else:
            return True

    def get(self, stuNo):
        cur = get_db().cur

        cur.execute("SELECT Student.stuNo,stuName,stuAge,Class.classNo,dormitoryNo FROM Student,Class,Department WHERE Student.classNo=Class.classNo AND Class.departNo=Department.departNo AND stuNo='%s'" % stuNo)
        items = cur.fetchone()
        print(items)

        cur.execute("SELECT * FROM JoinStatus WHERE stuNo='%s'" % stuNo)
        society_list = [x[1] for x in cur.fetchall()]

        if not items:
            return {'errCode': -1, 'status': '请求条目不存在'}
        else:
            return {'errCode': 0,
                    'status': 'OK',
                    'data': {'stuNo': items[0],
                             'stuName': items[1],
                             'stuAge': items[2],
                             'classNo': items[3],
                             'dormitory': items[4],
                             'society': society_list
                             }
                    }

    def put(self, stuNo):
        db = get_db()
        db.autocommit = False
        cur = get_db().cur
        args = parser_studentItem.parse_args()

        if not self.checkIfExist(stuNo):
            return {'errCode': -1, 'status': '操作的学生不存在'}

        try:
            cur.execute("UPDATE Student SET stuName='%s',"
                        "stuAge = %d,"
                        "classNo = '%s'"
                        "WHERE stuNo='%s';" % (args['stuName'], args['stuAge'], args['classNo'], stuNo))
            db.commit()
        except Error as e:
            db.rollback()
            return {'errCode': -1, 'status': str(e)}

        return {'errCode': 0, 'status': 'OK'}, 200

    def delete(self, stuNo):  # 删除
        if not self.checkIfExist(stuNo):
            return {'errCode': -1, 'status': '操作的学生不存在'}
        db = get_db()
        cur = get_db().cur
        try:
            cur.execute(
                "DELETE FROM JoinStatus WHERE stuNo='%s';" % stuNo)
            cur.execute(
                "DELETE FROM Student WHERE stuNo='%s';" % stuNo)
            db.commit()
        except Error as e:
            return {'errCode': -1, 'status': str(e)}
        return {'errCode': 0, 'status': 'OK'}, 200


parser_student = parser_studentItem.copy()
parser_student.add_argument('stuNo', required=True,
                            type=str, help="stuNo not provide.")


class student(Resource):
    def get(self):
        cur = get_db().cur
        cur.execute("SELECT stuNo,stuName,stuAge,classNo FROM Student;")

        res = {'errCode': 0,
               'status': 'OK',
               'data': [{'stuNo': item[0],
                         'stuName': item[1],
                         'stuAge': item[2],
                         'classNo':item[3]
                         }
                        for item in cur.fetchall()]}
        return res

    def post(self):
        args = parser_student.parse_args()
        db = get_db()
        cur = get_db().cur

        try:
            print(args['classNo'])
            cur.execute("INSERT INTO Student(stuNo, stuName, stuAge, classNo) "
                        "VALUES('%s', '%s', %d, '%s');" %
                        (args['stuNo'], args['stuName'], args['stuAge'], args['classNo']))
            db.commit()
        except Error as e:
            return {'errCode': -1, 'status': str(e)}
        return {'errCode': 0, 'status': 'OK'}, 200


parser_soc = reqparse.RequestParser()
parser_soc.add_argument(
    'societyNo', required=True, type=list, location='json', help="societyNo not provide.")


class sockety_m(Resource):
    def put(self, stuNo):
        db = get_db()
        db.autocommit = False
        cur = get_db().cur

        args = parser_soc.parse_args()

        cur.execute("SELECT * FROM JoinStatus WHERE stuNo='%s'" % stuNo)
        society_now = [x[1] for x in cur.fetchall()]
        try:
            if args['societyNo']:
                # edit JoinStatus
                # ToDo: 不知道为什么单次出错不发生异常
                for society in args['societyNo']:
                    if int(society) not in society_now:
                        cur.execute(
                            "INSERT INTO JoinStatus(stuNo, societyNo, joinYear) VALUES('%s',%d, '%s');" % (stuNo, int(society), datetime.datetime.now().year))
                for society in society_now:
                    if int(society) not in args['societyNo']:
                        cur.execute(
                            "DELETE FROM JoinStatus WHERE stuNo=%s AND societyNo=%d;" % (stuNo, int(society)))
            else:
                cur.execute(
                    "DELETE FROM JoinStatus WHERE stuNo=%s;" % (stuNo))
            db.commit()
        except Error as e:
            return {'errCode': -1, 'status': str(e)}
        return {'errCode': 0, 'status': 'OK'}, 200
