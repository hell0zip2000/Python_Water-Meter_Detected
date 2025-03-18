import mysql.connector

class DatabaseConnect:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="quanlynuoc"
            )
            self.cursor = self.conn.cursor(dictionary=True) 
        except mysql.connector.Error as err:
            print(f"Lỗi kết nối database: {err}")
            self.conn = None
            self.cursor = None
    
    def fetch_one(self, query, params=None):
        """Lấy một bản ghi"""
        if self.cursor:
            self.cursor.execute(query, params)
            return self.cursor.fetchone()
        return None

    def fetch_all(self, query, params=None):
        """Lấy tất cả bản ghi"""
        if self.cursor:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        return None
    def execute(self, query, params=None):
            try:
                self.cursor.execute(query, params)
                self.conn.commit()  # Quan trọng! Ghi thay đổi vào database
                return True
            except MySQLdb.Error as e:
                print(f"Lỗi truy vấn: {e}")
                return False

    def close(self):
        """Đóng kết nối"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
