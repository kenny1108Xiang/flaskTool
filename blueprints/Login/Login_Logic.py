import sqlite3

class Login_Class:
    def Login(self, account, password):
        """
        輸入帳號與密碼後\n
        若找到，會返回 id, username, permission
        型態為tuple
        """
        conn = sqlite3.connect('database/auth.db')
        cursor = conn.cursor()

        cursor.execute("SELECT id, username, permission FROM userData WHERE account = ? AND password = ?", (account, password))
        result = cursor.fetchone()

        conn.close()

        if result:
            print("User Login:", result[1])
            return result
        else:
            print("User Login Fail.")
            return None