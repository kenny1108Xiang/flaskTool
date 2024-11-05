from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Email
from flask import render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash
from ...email_sender import send_email
import secrets
import string

from . import Register_bp

import sqlite3

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    account = StringField('Account', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email(message="請輸入有效的Email")])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password', message='密碼不相同')
    ])
    submit = SubmitField('Register')

def generate_secure_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))


def Register(username, account, password, email):
    conn = sqlite3.connect('database/auth.db')
    cursor = conn.cursor()
    try:
            cursor.execute('''
            INSERT INTO userData (username, account, password, email)
            VALUES (?, ?, ?, ?)
            ''', (username, account, password, email))
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
        email = form.email.data
        check = generate_secure_code()
        try:
            send_email(email, check)
            ##問題1，已經成功發送email與check驗證碼到收件者的信箱，但前須做的是註冊按鈕按下後，確認是否為本人的email若是，則完成註冊剩下流程(將資料插入資料庫中)、接著回到Login_Page重新登入
            ##問題2，若使用者輸入錯誤或發生不可預期的錯誤導致後續不能順利將該使用者註冊到資料庫，需重新導向到註冊網頁，且顯示"email可能不存在"
            ##問題3，尚未修改Forgot的程式碼

        except Exception as e:
            print(e)
            flash("傳送驗證碼失敗")
            return render_template('auth/Register.html', form=form)
        
        username = form.username.data
        account = form.account.data
        password = generate_password_hash(form.password.data)
        

        result = Register(username, account, password, email)
        if result == "duplicate_account_password":
            flash('帳號與密碼有重複的人使用', 'danger')
        else:
            flash("註冊成功，請重新登入", 'success')
            return redirect(url_for('Login.Login_Page'))

        
    return render_template('auth/Register.html', form=form)

