import os

from flask import Flask

def create_app():
    application = Flask(__name__)

    application.config.from_mapping(
        SECRET_KEY = 'mikey'
        , DATABASE_HOST = os.environ.get('FLASK_DATABASE_HOST')
        , DATABASE_PASSWORD = os.environ.get('FLASK_DATABASE_PASSWORD')
        , DATABASE_USER = os.environ.get('FLASK_DATABASE_USER')
        , DATABASE = os.environ.get('FLASK_DATABASE')
    )

    from . import database
    database.initializeApp(application)

    from . import authentication
    application.registe.blueprint(authentication.bluePrint)

    @application.route('/hola')
    def hola():
        return 'Hola mundo'

    return application
