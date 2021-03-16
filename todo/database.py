import mysql.connector

import click
from flask import current_app, g as global
from flask.cli import with_appcontext
from .scheme import instructions

def getDatabase():
    if 'database' not in global:
        global.database = mysql.connector.connect(
            host = current_app.config['DATABASE_HOST']
            , user = current_app.config['DATABASE_USER']
            , password = current_app.config['DATABASE_PASSWORD']
            , database = current_app.config['DATABASE']
        )

        global.cursor = global.database.cursor(dictionary = True)
    return global.database, global.cursor

def closeDatabase(e = None)
    database = global.pop('database', None)

    if database is not None:
        database.close()

def init_app(app)
    app.teardown_appcontext(closeDatabase)
