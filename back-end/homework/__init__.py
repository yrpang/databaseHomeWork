import os
from flask import Flask
from flask.globals import current_app


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE_USER='root',
        DATABASE_HOST='cdb-n3duly12.bj.tencentcdb.com',
        DATABASE_NAME='homework',
        DATABASE_PASSWD='database2020__',
        DATABASE_PORT=10065
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from .api import api_bp
    app.register_blueprint(api_bp)

    @app.route('/')
    def hello():
        if(app.config.get('SHOWINFO', None)):
            return '环境配置正常，请开始开发，不要忘记DDL！'
        else:
            return '线上环境'

    return app
