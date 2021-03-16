import mysql.connector

import click
from flask import current_app, g
from flask.cli import with_appcontext
from .schema import instructions

def getDatabase():
    if 'database' not in g:
        g.database = mysql.connector.connect(
            host = current_app.config['DATABASE_HOST']
            , user = current_app.config['DATABASE_USER']
            , password = current_app.config['DATABASE_PASSWORD']
            , database = current_app.config['DATABASE']
        )

        g.cursor = g.database.cursor(dictionary = True)
    return g.database, g.cursor

def closeDatabase(e = None):
    database = g.pop('database', None)

    if database is not None:
        database.close()

def initializeDatabase():
    database, cursor = getDatabase()

    for instruction in instructions:
        cursor.execute(instruction)

    database.commit()

@click.command('init-db')
@with_appcontext
def initializeDatabaseCommand():
    initializeDatabase()
    click.echo('Bse de datos inicializada')

def initializeApp(aplication):
    aplication.teardown_appcontext(closeDatabase)
    aplication.cli.add_command(initializeDatabaseCommand)