import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

def send_email(recipient_email, subject, body):
    sender_email = 'denny0979539212@gmail.com'
    sender_password = os.getenv('sender_password')  # 從環境變數獲取應用程式密碼

    # 設定 SMTP 伺服器資訊
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587  # Gmail 使用 587

    try:
        # 建立郵件物件
        message = MIMEMultipart()
        message['From'] = 'Flask Tool <denny0979539212@gmail.com>'
        message['To'] = recipient_email
        message['Subject'] = subject

        # 添加郵件內容
        message.attach(MIMEText(body, 'plain'))

        # 連接到 SMTP 伺服器並登入
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # 啟用 TLS 加密
            server.login(sender_email, sender_password)  # 使用應用程式密碼登入
            server.sendmail(sender_email, recipient_email, message.as_string())  # 傳送郵件

        print("郵件傳送成功！")
        return True  # 傳送成功，回傳 True
    except Exception as e:
        print(f"郵件傳送失敗：{e}")
        return False  # 傳送失敗，回傳 False
