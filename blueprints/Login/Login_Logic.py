from werkzeug.security import check_password_hash
import sqlite3

class Login_Class:
    def Login(self, account):
        """
        輸入帳號後\n
        若找到，會返回 id, username, permission, password_hash
        型態為tuple
        """
        conn = sqlite3.connect('database/auth.db')
        cursor = conn.cursor()

        # 根據 account 查詢使用者資料
        cursor.execute("SELECT id, username, permission, password FROM userData WHERE account = ?", (account,))
        result = cursor.fetchone()

        conn.close()

        if result:
            print("User Found:", result[1])
            return result  # 返回資料庫中的加密密碼
        else:
            print("User Login Fail.")
            return None
