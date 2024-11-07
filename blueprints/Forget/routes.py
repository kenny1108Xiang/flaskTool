from . import Forgot_bp
from flask import redirect, url_for, render_template, flash, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Regexp
from email_sender import send_email
import secrets
import string
import sqlite3
from werkzeug.security import check_password_hash

class EmailForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(message="請填寫電子郵件地址。"), 
        Email(message="請輸入有效的電子郵件地址。")
    ])
    submit = SubmitField('送出')

class CheckForm(FlaskForm):
    verification_code = StringField(
        '驗證碼',
        validators=[
            DataRequired(message="驗證碼為必填欄位。"),
            Length(min=6, max=6, message="驗證碼必須為 6 個字元。"),
            Regexp(
                '^[A-Za-z0-9]{6}$',
                message="驗證碼只能包含英文字母和數字。"
            )
        ],
        render_kw={"placeholder": "輸入驗證碼"}
    )
    
    submit = SubmitField('驗證')

def generate_secure_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

def search_email(email, code):
    conn = sqlite3.connect('database/auth.db')
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM userData WHERE email = ?", (email,))
    result = cursor.fetchone()

    if result:
        cursor.execute("UPDATE userData SET code = ? WHERE email = ?", (code, email))
        conn.commit()
        conn.close()
        return "Done"
    else:
        conn.close()
        return "None"


@Forgot_bp.route('/', methods=['POST', 'GET'])
def Forgot_Page():
    form = EmailForm()
    if form.validate_on_submit():
        user_email = form.email.data
        code = generate_secure_code(length=6)
        result = search_email(user_email, code)
        if result == "Done":
            send_email(user_email, "復原碼", code)
            session['email'] = user_email
            return redirect(url_for('Forgot.Check_Page'))
    return render_template('auth/Forgot.html', form=form)

@Forgot_bp.route('/Check', methods=['POST', 'GET'])
def Check_Page():
    form = CheckForm()

    if form.validate_on_submit():
        get_code = form.verification_code.data
        conn = sqlite3.connect('database/auth.db')
        cursor = conn.cursor()

        # 從資料庫檢查驗證碼
        cursor.execute("SELECT username, password FROM userData WHERE code = ?", (get_code,))
        result = cursor.fetchone()
        print(result)


        if result:
            username, password = result
            result = cursor.execute("SELECT username, password FROM userData WHERE email=?", (session['email'],))
            conn.close()
            send_email(session['email'], "復原碼", f"帳號：{username}\n密碼：{check_password_hash(password)}")
            """
            因為使用generate_password_hash方法,此方法為單向加密'哈希處理'，所以是不可逆的，只能重設密碼
            
            """
            session.clear()
            flash("發送帳號密碼到您的電子信箱")
            return redirect(url_for('Login.Login_Page'))
        else:
            flash("驗證碼錯誤")
            return redirect(url_for('Forgot.Check_Page'))
    return render_template('auth/check.html', form=form, mode="Forgot")
