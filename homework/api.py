from configparser import Error
from flask import Blueprint, flash, g
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from homework.db import get_db

api_bp = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_bp)


# 下面为dormitory相关api的实现
parser_dormitoryItem = reqparse.RequestParser()
parser_dormitoryItem.add_argument('dormitoryName', required=True,
                                  type=str, help="dormitoryName not provide.")


class dormitoryItem(Resource):
    def checkIfExist(self, dormitoryNo):
        cur = get_db().cur
        cur.execute("SELECT * FROM Dormitory WHERE dormitoryNo='%s'" %
                    dormitoryNo)
        if(len(cur.fetchall()) < 1):
            abort(404, message={'errCode': -1, 'status': '操作的宿舍不存在'})

    def get(self, dormitoryNo):
        cur = get_db().cur

        cur.execute(
            "SELECT * FROM Dormitory WHERE dormitoryNo='%s'" % (dormitoryNo))
        items = cur.fetchone()
        print(items)
        if not items:
            return {'errCode': -1, 'status': '请求条目不存在'}
        else:
            return {'errCode': 0, 'status': 'OK', 'data': {'dormitoryNo': items[0], 'dormitoryName': items[1]}}

    def put(self, dormitoryNo):
        db = get_db()
        cur = get_db().cur
        args = parser_dormitoryItem.parse_args()

        self.checkIfExist(dormitoryNo)

        try:
            cur.execute("UPDATE Dormitory SET dormitoryName='%s' WHERE dormitoryNo='%s';" % (
                args['dormitoryName'], dormitoryNo))
            db.commit()
        except Error:
            return {'errCode': -1, 'status': '执行错误'}
        return {'errCode': 0, 'status': 'OK'}, 200

    def delete(self, dormitoryNo):
        self.checkIfExist(dormitoryNo)
        db = get_db()
        cur = get_db().cur

        try:
            cur.execute(
                "DELETE FROM Dormitory WHERE dormitoryNo='%s';" % dormitoryNo)
            db.commit()
        except Error:
            return {'errCode': -1, 'status': '执行错误'}
        return {'errCode': 0, 'status': 'OK'}, 200


parser_dormitory = parser_dormitoryItem.copy()
parser_dormitory.add_argument(
    'dormitoryNo', required=True, type=str, help="dormitoryNo not provide.")


class dormitory(Resource):
    def get(self):
        cur = get_db().cur
        cur.execute("SELECT * FROM Dormitory;")
        res = {'errCode': 0, 'status': 'OK', 'data': [
            {'dormitoryNo': item[0], 'dormitoryName':item[1]} for item in cur.fetchall()]}
        return res

    def post(self):
        args = parser_dormitory.parse_args()
        db = get_db()
        cur = get_db().cur

        try:
            cur.execute("INSERT INTO Dormitory(dormitoryNo, dormitoryName) VALUES('%s', '%s');" % (
                args['dormitoryNo'], args['dormitoryName']))
            db.commit()
        except Error:
            return {'errCode': -1, 'status': '执行错误'}
        return {'errCode': 0, 'status': 'OK'}, 200


api.add_resource(dormitory, '/dormitory')
api.add_resource(dormitoryItem, '/dormitory/<string:dormitoryNo>')


# 下面为department的api的实现
parser_departmentItem = reqparse.RequestParser()
parser_departmentItem.add_argument('departName', required=True,
                                   type=str, help="departName not provide.")
parser_departmentItem.add_argument('departOffice', required=True,
                                   type=str, help="departOffice not provide.")
parser_departmentItem.add_argument('departNum', required=True,
                                   type=int, help="departNum not provide.")
parser_departmentItem.add_argument('dormitoryNo', required=True,
                                   type=str, help="dormitoryNo not provide.")   # TO BE DELETE


class departmentItem(Resource):
    def checkIfExist(self, departNo):  # 查询是否存在
        cur = get_db().cur

        cur.execute("SELECT * FROM Department WHERE departNo='%s'" % departNo)
        if(len(cur.fetchall()) < 1):
            abort(404, message={'errCode': -1, 'status': '操作的系不存在'})

    def get(self, departNo):
        cur = get_db().cur

        cur.execute("SELECT * FROM Department WHERE departNo='%s'" % departNo)
        items = cur.fetchone()
        print(items)
        if not items:
            return {'errCode': -1, 'status': '请求条目不存在'}
        else:
            return {'errCode': 0, 'status': 'OK', 'data': {'departNo': items[0], 'departName': items[1], 'departOffice': items[2], 'departNum': items[3], 'dormitoryNo': items[4]}}

    def put(self, departNo):  # 增加
        db = get_db()
        cur = get_db().cur
        args = parser_departmentItem.parse_args()

        self.checkIfExist(departNo)

        try:
            cur.execute("UPDATE Department SET departName='%s',departOffice = '%s',departNum = '%d',dormitoryNo = '%s' WHERE departNo='%s';" % (
                args['departName'], args['departOffice'], args['departNum'], args['dormitoryNo'], departNo))
            db.commit()
        except Error:
            return {'errCode': -1, 'status': '执行错误'}
        return {'errCode': 0, 'status': 'OK'}, 200

    def delete(self, departNo):  # 删除
        self.checkIfExist(departNo)
        db = get_db()
        cur = get_db().cur

        try:
            cur.execute(
                "DELETE FROM Department WHERE departNo='%s';" % departNo)
            db.commit()
        except Error:
            return {'errCode': -1, 'status': '执行错误'}
        return {'errCode': 0, 'status': 'OK'}, 200


# 暂时不懂
parser_department = parser_departmentItem.copy()
parser_department.add_argument(
    'departNo', required=True, type=str, help="departNo not provide.")


class department(Resource):
    def get(self):
        cur = get_db().cur
        cur.execute("SELECT * FROM Department;")

        res = {'errCode': 0, 'status': 'OK', 'data': [
            {'departNo': item[0], 'departName': item[1], 'departOffice': item[2], 'departNum': item[3], 'dormitoryNo':item[4]} for item in cur.fetchall()]}
        return res

    def post(self):
        args = parser_department.parse_args()
        db = get_db()
        cur = get_db().cur

        try:
            cur.execute("INSERT INTO Department(departNo, departName,departOffice,departNum,dormitoryNo) VALUES('%s', '%s', '%s', '%d','%s');" % (
                args['departNo'], args['departName'], args['departOffice'], args['departNum'], args['dormitoryNo']))
            db.commit()
        except Error:
            return {'errCode': -1, 'status': '执行错误'}
        return {'errCode': 0, 'status': 'OK'}, 200


api.add_resource(department, '/department')
api.add_resource(departmentItem, '/department/<string:departNo>')



# 下面为student的api的实现(Hejia Chen)
parser_studentItem = reqparse.RequestParser()
parser_studentItem.add_argument('stuNo', required=True, type=str, help="stuNo not provide.")
parser_studentItem.add_argument('stuName', required=True, type=str, help="stuName not provide.")
parser_studentItem.add_argument('stuAge', required=True, type=int, help="stuAge not provide.")
parser_studentItem.add_argument('departNo', required=True, type=str, help="departNo not provide.")
parser_studentItem.add_argument('classNo', required=True, type=str, help="classNo not provide.")
parser_studentItem.add_argument('dormitoryNo', required=True, type=str, help="dormitoryNo not provide.")

class studentItem(Resource):
    def checkIfExist(self, stuNo):  # 查询是否存在
        cur = get_db().cur

        cur.execute("SELECT * FROM Student WHERE stuNo='%s'" % stuNo)
        if(len(cur.fetchall()) < 1):
            abort(404, message={'errCode': -1, 'status': '操作的系不存在'})

    def get(self, stuNo):
        cur = get_db().cur

        cur.execute("SELECT * FROM Student WHERE stuNo='%s'" % stuNo)
        items = cur.fetchone()
        print(items)
        if not items:
            return {'errCode': -1, 'status': '请求条目不存在'}
        else:
            return {'errCode': 0,
                    'status': 'OK',
                    'data': {'stuNo': items[0],
                             'stuName': items[1],
                             'stuAge': items[2],
                             'departNo': items[3],
                             'classNo': items[4],
                             'dormitoryNo': items[5]}
                    }

    def put(self, stuNo):  # 增加
        db = get_db()
        cur = get_db().cur
        args = parser_studentItem.parse_args()

        self.checkIfExist(stuNo)
        try:
            cur.execute("UPDATE Student SET stuName='%s',"
                        "stuAge = '%s',"
                        "departNo = '%d',"
                        "classNo = '%s', "
                        "dormitoryNo='%s'"
                        "WHERE stuNo='%s';" % (
                args['stuName'], args['stuAge'], args['departNo'], args['classNo'], args['dormitoryNo'], stuNo))
            db.commit()
        except Error:
            return {'errCode': -1, 'status': '执行错误'}
        return {'errCode': 0, 'status': 'OK'}, 200

    def delete(self, stuNo):  # 删除
        self.checkIfExist(stuNo)
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
parser_student.add_argument('stuNo', required=True, type=str, help="stuNo not provide.")


class student(Resource):
    def get(self):
        cur = get_db().cur
        cur.execute("SELECT * FROM Student;")

        res = {'errCode': 0,
               'status': 'OK',
               'data': [{'stuNo': item[0],
                         'stuName': item[1],
                         'stuAge': item[2],
                         'departNo': item[3],
                         'classNo':item[4],
                         'dormitoryNo': item[5]}
                        for item in cur.fetchall()]}
        return res

    def post(self):
        args = parser_student.parse_args()
        db = get_db()
        cur = get_db().cur

        try:
            cur.execute("INSERT INTO Student(stuNo, stuName,stuAge,departNo, classNo, dormitoryNo) "
                        "VALUES('%s', '%s', '%s', '%d','%s', '%s');" %
                        (args['stuNo'], args['stuName'], args['stuAge'],
                         args['departNo'], args['classNo'], args['dormitoryNo']))
            db.commit()
        except Error:
            return {'errCode': -1, 'status': '执行错误'}
        return {'errCode': 0, 'status': 'OK'}, 200


api.add_resource(student, '/student')
api.add_resource(departmentItem, '/student/<string:stuNo>')