from configparser import Error
from flask_restful import Resource, reqparse, abort
from homework.db import get_db

# 下面为association的api的实现 (tangkun)
parser_associationItem = reqparse.RequestParser()
parser_associationItem.add_argument('societyNo', required=True,
                                    type=str, help="societyNo not provide.")
parser_associationItem.add_argument('societyName', required=True,
                                    type=str, help="societyName not provide.")
parser_associationItem.add_argument('societyYear', required=True,
                                    type=int, help="societyYear not provide.")
parser_associationItem.add_argument('societyLoc', required=True,
                                    type=str, help="societyLoc not provide.")


class associationItem(Resource):
    def checkIfExist(self, societyNo):  # 查询是否存在
        cur = get_db().cur

        cur.execute("SELECT * FROM Association WHERE societyNo='%s'" %
                    societyNo)
        if(len(cur.fetchall()) < 1):
            abort(404, message={'errCode': -1, 'status': '操作的学会不存在'})

    def get(self, societyNo):
        cur = get_db().cur 

        cur.execute("SELECT societyNo,societyName,societyYear,societyLoc FROM Association WHERE societyNo='%s'" %
                    societyNo)
        items = cur.fetchone()
        if not items:
            return {'errCode': -1, 'status': '请求条目不存在'}
        else:
            return {'errCode': 0,
                    'status': 'OK',
                    'data': {'societyNo': items[0],
                             'societyName': items[1],
                             'societyYear': items[2],
                             'societyLoc': items[3]}
                    }

    def put(self, societyNo):
        db = get_db()
        cur = get_db().cur
        args = parser_associationItem.parse_args()

        self.checkIfExist(societyNo)

        try:
            cur.execute("UPDATE Association SET societyNo='%s',societyName = '%s',societyYear = '%d',societyLoc = '%s' WHERE societyNo='%s';" % (
                args['societyNo'], args['societyName'], args['societyYear'], args['societyLoc'], societyNo))
            db.commit()
        except Error:
            return {'errCode': -1, 'status': '执行错误'}
        return {'errCode': 0, 'status': 'OK'}, 200

    def delete(self, societyNo):  # 删除
        self.checkIfExist(societyNo)
        db = get_db()
        cur = get_db().cur

        try:
            cur.execute(
                "DELETE FROM Association WHERE societyNo='%s';" % societyNo)
            db.commit()
        except Error:
            return {'errCode': -1, 'status': '执行错误'}
        return {'errCode': 0, 'status': 'OK'}, 200


parser_association = parser_associationItem.copy()


class association(Resource):
    def get(self):
        cur = get_db().cur
        cur.execute("SELECT * FROM Association;")

        res = {'errCode': 0, 'status': 'OK', 'data': [
            {'societyNo': item[0], 'societyName': item[1], 'societyYear': item[2], 'societyLoc': item[3]} for item in cur.fetchall()]}
        return res

    def post(self):
        args = parser_association.parse_args()
        db = get_db()
        cur = get_db().cur

        try:
            cur.execute("INSERT INTO Association(societyNo, societyName,societyYear,societyLoc) VALUES('%s', '%d', '%s');" % (
                args['societyName'], args['societyYear'], args['societyLoc']))
            db.commit()
        except Error:
            return {'errCode': -1, 'status': '执行错误'}
        return {'errCode': 0, 'status': 'OK'}, 200
