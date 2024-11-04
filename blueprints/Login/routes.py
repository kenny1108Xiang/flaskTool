from . import Login_bp
from flask import render_template, redirect, url_for, flash, request, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from .Login_Logic import Login_Class

class LoginForm(FlaskForm):
    username = StringField('帳號', validators=[DataRequired()], render_kw={"placeholder": "Account"})
    password = PasswordField('密碼', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    submit = SubmitField('登入')

@Login_bp.route('/', methods=['POST', 'GET']) #/Login/
def Login_Page():
    form = LoginForm()
    if request.method == 'POST':
        if form.submit.data and form.validate():
            # 處理登入邏輯
            username = form.username.data
            password = form.password.data

            search = Login_Class()
            User_Data = search.Login(username, password)

            if User_Data:
                session["id"] = User_Data[0]
                session["username"] = User_Data[1]
                session["permission"] = User_Data[2]

                return f"登入成功，歡迎 {session["username"]}" #登入後的網頁
            
            else:
                flash("帳號或密碼錯誤")
                return redirect(url_for('Login.Login_Page'))

    return render_template('auth/Login.html', form=form)

