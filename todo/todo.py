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

def getTodo(id):
    database, cursor = getDatabase()

    cursor.execute(
        'SELECT t.id, t.description, t.completed, t.created_by, t.created_at, u.username '
        'FROM todo t JOIN user u ON t.created_by = u.id WHERE t.id = %s'
        , (id, )
    )

    todo = cursor.fetchone()

    if todo is None:
        abort(404, "El todo de id {0} no existe".format(id))

    return todo

@blueprint.route('/<int:id>/update', methods=['GET', 'POST'])
@loginRequired
def update(id):
    todo = getTodo(id)

    if request.method == 'POST':
        description = request.form['description']
        completed = True if request.form.get('completed') == 'on' else False
        error = None

        if not description:
            error = "La descripción es requerida."

        if error is not None:
            flash(error)
        else:
            database, cursor = getDatabase()

            cursor.execute(
                'UPDATE todo SET description = %s, completed = %s '
                'WHERE id = %s'
                , (description, completed, id)
            )

            database.commit()

            return redirect(url_for('todo.index'))

    return render_template('todo/update.html', todo=todo)


@blueprint.route('/<int:id>/delete', methods=['POST'])
@loginRequired
def delete(id):
    database, cursor = getDatabase()

    cursor.execute(
        'DELETE FROM todo WHERE id = %s'
        , (id,)
    )

    database.commit()

    return redirect(url_for('todo.index'))