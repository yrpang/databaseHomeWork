from .classM import ClassAll, classItem
from .society import association, associationItem
from .student import student, studentItem, sockety_m
# from .domitary import dormitory, dormitoryItem
from .department import department, departmentItem
from flask import Blueprint, flash, g
from flask_restful import Api, reqparse, Resource
from homework.db import get_db
from mysql.connector.errors import Error

api_bp = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_bp)

api.add_resource(department, '/department')
api.add_resource(departmentItem, '/department/<string:departNo>')

api.add_resource(association, '/society')
api.add_resource(associationItem, '/society/<string:societyNo>')

api.add_resource(student, '/student')
api.add_resource(studentItem, '/student/<string:stuNo>')

api.add_resource(ClassAll, '/class')
api.add_resource(classItem, '/class/<string:classNo>')

api.add_resource(sockety_m, '/student/society/<string:stuNo>')

# api.add_resource(dormitory, '/dormitory')
# api.add_resource(dormitoryItem, '/dormitory/<string:dormitoryNo>')

parser = reqparse.RequestParser()
parser.add_argument('old_No', required=True,
                    type=str, help="old_No not provide!")
parser.add_argument('new_No', required=True,
                    type=str, help="new_No not provide!")


class change_classNo(Resource):
    def post(self):
        db = get_db()
        args = parser.parse_args()
        cur = get_db().cur

        try:
            cur.execute('SELECT change_classNo(%s, %s)' %
                        (args['old_No'], args['new_No']))
            data = cur.fetchone()
            db.commit()
        except Error as e:
            return {'errCode': -1, 'status': str(e)}
        return {'errCode': 0, 'status': 'OK', 'data': data}, 200


api.add_resource(change_classNo, '/manage/changeClassNo')


class fixNumInfo(Resource):
    def get(self):
        db = get_db()
        cur = get_db().cur
        cur.execute('CALL FIXNUM')

        cur.execute('SELECT * FROM tmp_table')
        data = [
            {'departNo': item[0], 'departName': item[1], 'old_num': item[2], 'new_num': item[3]} for item in cur.fetchall()
        ]
        cur.execute('DROP TABLE IF EXISTS tmp_table')
        return {'errCode': 0, 'status': 'OK', 'data': data}, 200
