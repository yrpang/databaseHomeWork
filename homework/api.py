from flask import Blueprint, flash, g
from flask_restful import Api, Resource, url_for
from homework.db import get_db

api_bp = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_bp)


class getAllStudents(Resource):
    def get(self):
        return {'task': 'Say "Hello, World!"'}

api.add_resource(getAllStudents, '/')
