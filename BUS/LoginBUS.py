from Config.databaseConnect import DatabaseConnect

class LoginBUS:
    def __init__(self):
        self.db = DatabaseConnect()

    def check_login(self, username, password):
        query = f"SELECT * FROM taikhoan WHERE user = %s AND password = %s"
        params = (username, password)
        user = self.db.fetch_one(query, params)

        return user is not None  # Trả về True nếu đăng nhập thành công, False nếu thất bại
