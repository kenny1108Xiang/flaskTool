from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo
from flask import render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash

from . import Register_bp

import sqlite3

class RegistrationForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    account = StringField('Account', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password', message='密碼不相同')
    ])
    submit = SubmitField('Register')

def Register(username, account, password):
    conn = sqlite3.connect('database/auth.db')
    cursor = conn.cursor()
    try:
            cursor.execute('''
            INSERT INTO userData (username, account, password)
            VALUES (?, ?, ?)
            ''', (username, account, password))
            conn.commit()
    except sqlite3.IntegrityError as e:
        # 檢查錯誤訊息是否包含 UNIQUE 約束的錯誤
        if "UNIQUE constraint failed: users.account, users.password" in str(e):
            conn.close()
            return "duplicate_account_password"
        else:
            conn.close()
            raise e
    conn.close()
    return "success"



@Register_bp.route('/', methods=['GET', 'POST'])
def Register_Page():
    form = RegistrationForm()
    if form.validate_on_submit():  #  POST 與 表單驗證
        username = form.username.data
        account = form.account.data
        password = generate_password_hash(form.password.data)

        result = Register(username, account, password)
        if result == "duplicate_account_password":
            flash('帳號與密碼有重複的人使用', 'danger')
        else:
            flash("註冊成功，請重新登入", 'success')
            return redirect(url_for('Login.Login_Page'))

        
    return render_template('auth/Register.html', form=form)
