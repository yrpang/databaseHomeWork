import mysql.connector as mysqlcon

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        g.db = mysqlcon.connect(
            user=current_app.config['DATABASE_USER'],
            password=current_app.config['DATABASE_PASSWD'],
            host=current_app.config['DATABASE_HOST'],
            database=current_app.config['DATABASE_NAME'],
            port=current_app.config['DATABASE_PORT']
        )
        g.db.cur = g.db.cursor()

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    cur = get_db().cur
    with current_app.open_resource('schema.sql') as f:
        sql_list = f.read().split(b';')[:-1]
        for x in sql_list:
            if b'\n' in x:
                x = x.replace(b'\n', b'')

            sql_item = x.decode() + ";"
            cur.execute(sql_item)


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
