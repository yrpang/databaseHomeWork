from configparser import Error
from flask import Blueprint, flash, g
from flask_restful import Api, Resource, reqparse, fields, marshal_with
from homework.db import get_db

# 下面为department的api的实现
parser_departmentItem = reqparse.RequestParser()
parser_departmentItem.add_argument('departName', required=True,
                                   type=str, help="departName not provide.")
parser_departmentItem.add_argument('departOffice', required=True,
                                   type=str, help="departOffice not provide.")
parser_departmentItem.add_argument('dormitoryNo', required=True,
                                   type=str, help="dormitoryNo not provide.")


class departmentItem(Resource):
    def checkIfExist(self, departNo):
        cur = get_db().cur

        cur.execute("SELECT * FROM Department WHERE departNo='%s'" % departNo)
        if(len(cur.fetchall()) < 1):
            return False
        else:
            return True

    def get(self, departNo):
        cur = get_db().cur

        cur.execute(
            "SELECT departNo,departName,departOffice,departNum,dormitoryNo FROM Department WHERE departNo='%s'" % departNo)
        items = cur.fetchone()
        if not items:
            return {'errCode': -1, 'status': '请求条目不存在'}
        else:
            return {'errCode': 0, 'status': 'OK', 'data': {'departNo': items[0], 'departName': items[1], 'departOffice': items[2], 'departNum': items[3], 'dormitoryNo': items[4]}}

    def put(self, departNo):
        db = get_db()
        cur = get_db().cur
        args = parser_departmentItem.parse_args()

        if not self.checkIfExist(departNo):
            return {'errCode': -1, 'status': '操作的系不存在'}

        try:
            cur.execute("UPDATE Department SET departName='%s',departOffice = '%s',dormitoryNo = '%s' WHERE departNo='%s';" % (
                args['departName'], args['departOffice'], args['dormitoryNo'], departNo))
            db.commit()
        except Error:
            return {'errCode': -1, 'status': '执行错误'}
        return {'errCode': 0, 'status': 'OK'}, 200

    def delete(self, departNo):  # 删除
        if not self.checkIfExist(departNo):
            return {'errCode': -1, 'status': '操作的系不存在'}
        db = get_db()
        cur = get_db().cur

        try:
            cur.execute(
                "DELETE FROM Department WHERE departNo='%s';" % departNo)
            db.commit()
        except Error:
            return {'errCode': -1, 'status': '执行错误'}
        return {'errCode': 0, 'status': 'OK'}, 200


parser_department = parser_departmentItem.copy()


class department(Resource):
    def get(self):
        cur = get_db().cur
        cur.execute(
            "SELECT departNo,departName,departOffice,departNum,dormitoryNo FROM Department;")

        res = {'errCode': 0, 'status': 'OK', 'data': [
            {'departNo': item[0], 'departName': item[1], 'departOffice': item[2], 'departNum': item[3], 'dormitoryNo':item[4]} for item in cur.fetchall()]}
        return res

    def post(self):
        args = parser_department.parse_args()
        db = get_db()
        cur = get_db().cur

        try:
            cur.execute("INSERT INTO Department(departName,departOffice,dormitoryNo) VALUES('%s', '%s', '%s');" % (
                args['departName'], args['departOffice'], args['dormitoryNo']))
            db.commit()
        except Error:
            return {'errCode': -1, 'status': '执行错误'}
        return {'errCode': 0, 'status': 'OK'}, 200
