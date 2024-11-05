from functools import wraps
from flask import session, redirect, url_for

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            print('Not Allow')
            return redirect(url_for('Login.Login_Page'))
        return f(*args, **kwargs)
    return decorated_function
