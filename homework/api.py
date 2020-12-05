import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from homework.db import get_db

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/getAllStudents', methods=["GET"])
def getAllStudents():
    db = get_db()
    return 'hello'
