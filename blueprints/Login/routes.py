from . import Login_bp
from flask import render_template, redirect, url_for, request, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

from Login_Logic import Login_Class


class LoginForm(FlaskForm):
    username = StringField('帳號', validators=[DataRequired()], render_kw={"placeholder": "Account"})
    password = PasswordField('密碼', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    submit = SubmitField('登入')
    forgot = SubmitField('忘記?')
    back = SubmitField('返回')

@Login_bp.route('/Login', methods=['POST', 'GET'])
def Login_Page():
    form = LoginForm()
    if form.validate_on_submit():
        if form.forgot.data:
            return redirect(url_for('forgot_password'))
        elif form.back.data:
            return redirect(url_for('home'))
        elif form.submit.data:
            return redirect(url_for('Login_bp.Login_Method', username=form.username.data, password=form.password.data))
    return render_template('Login.html', form=form)


@Login_bp.route('/forgot')
def forgot_password():
    return "忘記密碼頁面"

@Login_bp.route('/')
def home():
    return "返回主頁面"

@Login_bp.route('/Login_Method', methods=['POST', 'GET'])
def Login_Method():
    # 從表單中獲取使用者的帳號和密碼
    username = request.args.get("username")
    password = request.args.get("password")

    # 使用 Login_Logic 類別進行驗證
    search = Login_Class()
    login_status = search.Login(username, password)

    # 根據驗證結果返回不同的訊息
    if login_status:
        return "登入成功，歡迎！"
    else:
        flash("登入失敗，帳號或密碼不正確")
        return redirect(url_for('Login_bp.Login_Page'))