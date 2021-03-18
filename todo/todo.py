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
    if request.method == 'POST':
        description = request.form['description']
        error = None

        if not description:
            error = 'Descripción es requerida.'

        if error is not None:
            flash(error)
        else:
            database, cursor = getDatabase()

            cursor.execute(
                'INSERT INTO todo (description, completed, created_by)'
                ' VALUES (%s, %s, %s)'
                , (description, False, g.user['id'])
            )

            database.commit()

            return redirect(url_for('todo.index'))

    return render_template('todo/create.html')

@blueprint.route('/<int:id>/update', methods=['GET', 'POST'])
@loginRequired
def update(id):
    return render_template('todo/update.html', todo={
        "description": "mi todo"
        , "id": 2
        , "completed": 1
    })


@blueprint.route('/<int:id>/delete', methods=['POST'])
@loginRequired
def delete(id):
    return ''