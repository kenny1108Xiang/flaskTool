from . import Login_bp
from flask import render_template, redirect, url_for, flash, request
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
            login_status = search.Login(username, password)

            if login_status:
                return "登入成功，歡迎！"
            else:
                flash("登入失敗，帳號或密碼不正確")
                return redirect(url_for('Login.Login_Page'))

    return render_template('auth/Login.html', form=form)

@Login_bp.route('/forgot')
def forgot_password():
    return render_template('auth/Forgot.html')

