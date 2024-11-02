from . import Login_bp
from flask import render_template

@Login_bp.route('/Login', methods=['POST', 'GET'])
def Login_Page():
    return render_template('Login.html')