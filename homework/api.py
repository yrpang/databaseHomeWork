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
