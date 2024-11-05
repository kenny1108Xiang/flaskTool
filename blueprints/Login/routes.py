from . import Login_bp
from flask import render_template, redirect, url_for, flash, request, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from .Login_Logic import Login_Class
from werkzeug.security import check_password_hash

class LoginForm(FlaskForm):
    username = StringField('帳號', validators=[DataRequired()], render_kw={"placeholder": "Account"})
    password = PasswordField('密碼', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    submit = SubmitField('登入')

@Login_bp.route('/', methods=['POST', 'GET'])  # /Login/
def Login_Page():
    form = LoginForm()
    if request.method == 'POST':
        if form.submit.data and form.validate():
            # 處理登入邏輯
            username = form.username.data
            password = form.password.data

            search = Login_Class()

            # 檢查是否是特定的測試帳號
            if username == 'kenny' and password == '1108':
                User_Data = search.Login(username)
                if password == User_Data[3]:
                    session["id"] = User_Data[0]
                    session["username"] = User_Data[1]
                    session["permission"] = User_Data[2]
                    return redirect(url_for('auth.auth_index', username=session["username"]))
                else:
                    flash("帳號或密碼錯誤")
                    return redirect(url_for('Login.Login_Page'))
            else:
                # 查詢資料庫中的使用者資料
                User_Data = search.Login(username)
                # 如果使用者存在且密碼匹配
                if User_Data and check_password_hash(User_Data[3], password):  # User_Data[3] 是加密密碼
                    session["id"] = User_Data[0]
                    session["username"] = User_Data[1]
                    session["permission"] = User_Data[2]

                    return redirect(url_for('auth.auth_index', username=session["username"]))
                else:
                    flash("帳號或密碼錯誤")
                    return redirect(url_for('Login.Login_Page'))

    return render_template('auth/Login.html', form=form)

