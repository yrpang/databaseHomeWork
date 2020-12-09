from .class import ClassAll, classItem
from .society import association, associationItem
from .student import student, studentItem
# from .domitary import dormitory, dormitoryItem
from .department import department, departmentItem
from flask import Blueprint, flash, g
from flask_restful import Api

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

# api.add_resource(dormitory, '/dormitory')
# api.add_resource(dormitoryItem, '/dormitory/<string:dormitoryNo>')
