from flask import (
    Blueprint, blueprints, flash, g, redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort
from todo.authentication import loginRequired
from todo.database import getDatabase

blueprint = Blueprint('todo', __name__)

@blueprint.route('/')
@loginRequired
def index():
    database, cursor = getDatabase()

    cursor.execute(
        'SELECT t.id, t.description, u.username, t.completed, t.created_at FROM todo t JOIN user u ON t.created_by = u.id ORDER BY created_at desc'
    )

    todos = cursor.fetchall()

    return render_template('todo/index.html', todos = todos)

@blueprint.route('/create', methods=['GET', 'POST'])
@loginRequired
def create():
    return ''

@blueprint.route('/update', methods=['GET', 'POST'])
@loginRequired
def update():
    return ''