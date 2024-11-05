from . import Forgot_bp
from flask import redirect, url_for, render_template, flash, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email
from ...email_sender import send_email
import secrets
import string
import sqlite3

class EmailForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('送出')

def generate_secure_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

def password_to_code(code):
    conn = sqlite3.connect('database/auth.db')
    cursor = conn.cursor()

    

@Forgot_bp.route('/', methods=['POST', 'GET'])
def Forgot_Page():
    return render_template('auth/Forgot.html')

@Forgot_bp.route('/send_email', methods=['POST'])
def email():
    form = EmailForm()
    if form.validate_on_submit():  # 表單提交並通過驗證
        user_email = form.email.data
        code = generate_secure_code()
        send_email(user_email, code)
        flash(f'密碼重置郵件已發送到 {email}!', 'success')
        return redirect(url_for('Forgot.Forgot_Page'))
    return redirect(url_for('Forgot.Forgot_Page'))