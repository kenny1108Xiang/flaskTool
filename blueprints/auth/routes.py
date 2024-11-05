from . import auth_bp
from flask import render_template, session, redirect, url_for, make_response, request
from check_Login import login_required

@auth_bp.route('/<username>', methods=['POST', 'GET'])
@login_required
def auth_index(username):
    if session['username'] != username:
        return redirect(url_for('Login.Login_Page'))
    response = make_response(render_template('auth/auth_index.html', username=username))
    # 設置防止緩存的 HTTP 標頭
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


@auth_bp.route('/Logout', methods=['GET', 'POST'])
@login_required
def Logout():
    session.clear()
    return redirect(url_for('Login.Login_Page'))
