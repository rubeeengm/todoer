import functools

from flask import (
    Blueprint, flash, g, render_template, request, url_for, session
)

from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import redirect

from todo.database import getDatabase

bluePrint = Blueprint(
    'auth', __name__, url_prefix='/auth'
)

@bluePrint.route('/register', methods=['GET', 'POST'])
def register():
    error = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        database, cursor = getDatabase()

        cursor.execute(
            'SELECT id FROM user WHERE username = %s', (username,)
        )

        if not username:
            error = 'Username es requerido'
        
        if not password:
            error = 'Password es requerido'
        elif cursor.fetchone() is not None:
            error = 'Usuario {} se encuenta registrado.'.format(username)

        if error is None:        
            cursor.execute(
                'INSERT INTO user (username, password) values (%s, %s)'
                , (username, generate_password_hash(password))
            )

            database.commit()

            return redirect(url_for('authentication.login'))

        flash(error)
    
    return render_template('auth/register.html')

@bluePrint.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['pasword']

        database, cursor = getDatabase()

        cursor.execute(
            'SELECT * FROM user WHERE username = %s', (username,)
        )

        user = cursor.fetchone()

        if user is None:
            error = 'Usuario y/o contraseña inválida'
        elif not check_password_hash(user['password'], password):
            error = 'Usuario y/o contraseña inválida'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')