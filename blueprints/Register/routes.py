from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Email, Length, Regexp
from flask import render_template, flash, redirect, url_for, session
from werkzeug.security import generate_password_hash
from email_sender import send_email
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


def Register(username, account, password, email):
    try:
        conn = sqlite3.connect('database/auth.db')
        cursor = conn.cursor()

        cursor.execute("INSERT INTO userData (username, account, password, email)\
                        VALUES (?, ?, ?, ?)",\
                        (username, account, password, email))
        conn.commit()
    except sqlite3.IntegrityError as e:
        # 檢查是否是 UNIQUE 約束錯誤
        if 'UNIQUE constraint failed' in str(e):
            # 根據具體欄位給出錯誤提示
            if 'userData.account' in str(e):
                flash("此帳號已被使用，請使用其他帳號。")
            elif 'userData.email' in str(e):
                flash("此電子郵件已註冊，請使用其他電子郵件。")
            else:
                flash("帳號和密碼的組合已存在，請重新嘗試。")
        else:
            flash("發生其他資料庫錯誤，請稍後再試。")
        
    finally:
        conn.close()


@Register_bp.route('/', methods=['GET', 'POST'])
def Register_Page():
    form = RegistrationForm()
    if form.validate_on_submit():
        email = form.email.data

        try:
            # 使用 with 管理資料庫連接，確保操作後自動關閉連接
            with sqlite3.connect('database/auth.db') as conn:
                cursor = conn.cursor()

                # 檢查 email 是否已存在
                cursor.execute("SELECT 1 FROM userData WHERE email = ?", (email,))
                if cursor.fetchone():
                    flash("該電子郵件已被註冊")
                    return render_template('auth/Register.html', form=form)

                # 發送驗證碼
                check = generate_secure_code()
                if not send_email(email, "註冊驗證碼", check):
                    flash("傳送驗證碼失敗，請稍後再試")
                    return render_template('auth/Register.html', form=form)

                # 插入暫存註冊資料並提交
                cursor.execute("INSERT INTO temp_registrations (username, account, password, code) VALUES (?, ?, ?, ?)",
                                (form.username.data, form.account.data, form.password.data, check))
                conn.commit()

                # 儲存 email 至 session，便於下一步確認身份
                session['email'] = email
                return redirect(url_for('Register.Check_Page'))

        except Exception as e:
            print(e)
            flash("系統錯誤，請稍後再試或聯絡管理員")
            return render_template('auth/Register.html', form=form)

    # 初次加載或驗證失敗時，重新渲染註冊頁面
    return render_template('auth/Register.html', form=form)


@Register_bp.route('/Check', methods=['POST', 'GET'])
def Check_Page():
    form = CheckForm()

    # 如果是 POST 請求且表單通過驗證
    if form.validate_on_submit():
        get_code = form.verification_code.data

        conn = sqlite3.connect('database/auth.db')
        cursor = conn.cursor()

        # 從資料庫檢查驗證碼
        cursor.execute("SELECT code FROM temp_registrations")
        result = cursor.fetchone()
        conn.close()

        # 比對驗證碼
        if result is None or get_code != result[0]:
            flash("驗證碼錯誤")
            return redirect(url_for('Register.Check_Page'))

        # 驗證碼正確的情況
        conn = sqlite3.connect('database/auth.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM temp_registrations")
        registration_data = cursor.fetchone()
        
        Register(registration_data[0], registration_data[1], generate_password_hash(registration_data[2]), session['email'])
        session.clear()

        # 刪除 temp_registrations 中的所有資料
        cursor.execute("DELETE FROM temp_registrations")
        conn.commit()
        conn.close()

        flash("帳號已註冊完畢，請重新登入")
        return redirect(url_for('Login.Login_Page'))

    # 如果是 GET 請求，或 POST 表單驗證失敗，直接顯示表單
    return render_template('auth/check.html', form=form, mode="Register")

