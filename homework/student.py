from configparser import Error
from flask_restful import Resource, reqparse, abort
from homework.db import get_db


# 下面为student的api的实现(Hejia Chen)
parser_studentItem = reqparse.RequestParser()
parser_studentItem.add_argument(
    'stuNo', required=True, type=str, help="stuNo not provide.")
parser_studentItem.add_argument(
    'stuName', required=True, type=str, help="stuName not provide.")
parser_studentItem.add_argument(
    'stuAge', type=int, help="stuAge not provide.")
parser_studentItem.add_argument(
    'departNo', required=True, type=str, help="departNo not provide.")
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

        cur.execute("SELECT * FROM Student WHERE stuNo='%s'" % stuNo)
        items = cur.fetchone()
        if not items:
            return {'errCode': -1, 'status': '请求条目不存在'}
        else:
            return {'errCode': 0,
                    'status': 'OK',
                    'data': {'stuNo': items[0],
                             'stuName': items[1],
                             'stuAge': items[2],
                             'classNo': items[3]
                             }
                    }

    def put(self, stuNo):  # 增加
        db = get_db()
        cur = get_db().cur
        args = parser_studentItem.parse_args()

        if not self.checkIfExist(stuNo):
            return {'errCode': -1, 'status': '操作的系不存在'}

        try:
            cur.execute("UPDATE Student SET stuName='%s',"
                        "stuAge = '%d',"
                        "departNo = '%s',"
                        "classNo = '%s', "
                        "dormitoryNo='%s'"
                        "WHERE stuNo='%s';" % (args['stuName'], args['stuAge'], args['departNo'],
                                               args['classNo'], args['dormitoryNo'], stuNo))
            db.commit()
        except Error:
            return {'errCode': -1, 'status': '执行错误'}
        return {'errCode': 0, 'status': 'OK'}, 200

    def delete(self, stuNo):  # 删除
        if not self.checkIfExist(stuNo):
            return {'errCode': -1, 'status': '操作的系不存在'}
        db = get_db()
        cur = get_db().cur
        try:
            cur.execute(
                "DELETE FROM Student WHERE stuNo='%s';" % stuNo)
            db.commit()
        except Error:
            return {'errCode': -1, 'status': '执行错误'}
        return {'errCode': 0, 'status': 'OK'}, 200


parser_student = parser_studentItem.copy()
parser_student.add_argument('stuNo', required=True,
                            type=str, help="stuNo not provide.")


class student(Resource):
    def get(self):
        cur = get_db().cur
        cur.execute("SELECT * FROM Student;")

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
            cur.execute("INSERT INTO Student(stuNo, stuName, stuAge, departNo, classNo, dormitoryNo) "
                        "VALUES('%s', '%s', '%d', '%s','%s', '%s');" %
                        (args['stuNo'], args['stuName'], args['stuAge'],
                         args['departNo'], args['classNo'], args['dormitoryNo']))
            db.commit()
        except Error:
            return {'errCode': -1, 'status': '执行错误'}
        return {'errCode': 0, 'status': 'OK'}, 200
