from configparser import Error
from flask import Blueprint, flash, g
from flask_restful import Api, Resource, reqparse, fields, marshal_with, abort
from homework.db import get_db

# 下面为_Class的api的实现
parser_classItem = reqparse.RequestParser()
parser_classItem.add_argument('className', required=True,
                              type=str, help="className not provide.")
parser_classItem.add_argument('classYear', required=True,
                              type=str, help="classYear not provide.")
parser_classItem.add_argument('departNo', required=True,
                              type=int, help="departNo not provide.")


class classItem(Resource):
    def checkIfExist(self, classNo):  # 查询是否存在
        cur = get_db().cur

        cur.execute("SELECT * FROM Class WHERE classNo='%s'" % classNo)
        if(len(cur.fetchall()) < 1):
            abort(404, {'errCode': -1, 'status': '不存在'})

    def get(self, classNo):
        cur = get_db().cur

        cur.execute("SELECT classNo, className, classYear, classNum, departName FROM Class, Department WHERE classNo='%s' AND Class.departNo=Department.departNo" % classNo)
        items = cur.fetchone()
        print(items)
        if not items:
            return {'errCode': -1, 'status': '请求条目不存在'}
        else:
            return {'errCode': 0, 'status': 'OK', 'data': {'classNo': items[0], 'className': items[1], 'classYear': items[2], 'classNum': items[3], 'departName': items[4]}}

    def put(self, classNo):
        db = get_db()
        cur = get_db().cur
        args = parser_classItem.parse_args()

        self.checkIfExist(classNo)

        try:
            cur.execute("UPDATE Class SET className='%s', classYear = %d, departNo = %d, WHERE classNo='%s';" % (
                args['className'], args['classYear'], args['departNo'], classNo))
            db.commit()
        except Error:
            return {'errCode': -1, 'status': '执行错误'}
        return {'errCode': 0, 'status': 'OK'}, 200

    def delete(self, classNo):  # 删除
        self.checkIfExist(classNo)
        db = get_db()
        cur = get_db().cur

        try:
            cur.execute(
                "DELETE FROM _Class WHERE classNo='%s';" % classNo)
            db.commit()
        except Error:
            return {'errCode': -1, 'status': '执行错误'}
        return {'errCode': 0, 'status': 'OK'}, 200


parser__Class = parser_classItem.copy()
parser__Class.add_argument('classNo', required=True,
                           type=str, help="classNo not provide.")


class ClassAll(Resource):
    def get(self):
        cur = get_db().cur
        cur.execute(
            "SELECT classNo, className, classYear, classNum, departName FROM Class, Department WHERE Class.departNo=Department.departNo")

        res = {'errCode': 0, 'status': 'OK', 'data': [
            {'classNo': item[0], 'className': item[1], 'classYear': item[2], 'classNum': item[3], 'departName':item[4]} for item in cur.fetchall()]}
        return res

    def post(self):
        args = parser__Class.parse_args()
        db = get_db()
        cur = get_db().cur

        try:
            cur.execute("INSERT INTO Class(classNo, className, classYear, departNo) VALUES('%s', '%s', %d,  %d);" % (
                args['classNo'], args['className'], args['classYear'], args['departNo']))
            db.commit()
        except Error:
            return {'errCode': -1, 'status': '执行错误'}
        return {'errCode': 0, 'status': 'OK'}, 200
