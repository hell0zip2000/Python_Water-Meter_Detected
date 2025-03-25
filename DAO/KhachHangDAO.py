# Data Access Object/ interact with SQL database with insert, delete, update. taken from DTO through BUS 
from Config.databaseConnect import get_conn
from DTO.KhachHangDTO import KhachHangDTO  # Import lớp DTO
from datetime import datetime
class KhachHangDAO:
    def __init__(self):
        self.conn = get_conn()
        self.cursor = self.conn.cursor()

    def get_all(self):
        listKH = []
        """Lấy thông tin user theo ID"""
        self.cursor.execute("SELECT * FROM customers")
        rows = self.cursor.fetchall()
        for row in rows:
            user_dto = KhachHangDTO(row[0], row[1], row[2], row[3], row[4],row[5])  # transform useless tuples into DTO
            listKH.append(user_dto)  # Thêm vào danh sách
        return listKH

    def get_user(self, id):
        """Lấy thông tin user theo ID"""
        self.cursor.execute("SELECT * FROM customers WHERE id = %s", (id,))
        row = self.cursor.fetchone()
        if row:
            return KhachHangDTO(row[0], row[1], row[2], row[3], row[4])  # Trả về đối tượng DTO
        return None

    def insert_user(self, name, email, phone, address):
        """Thêm user mới"""
        self.cursor.execute("SELECT MAX(id) FROM customers")
        max_id = self.cursor.fetchone()[0]
        new_id = max_id + 1 if max_id is not None else 1
        today = datetime.today().strftime('%Y-%m-%d')
        sql = "INSERT INTO customers (id, name, email, phone, address, created_at) VALUES (%s, %s, %s, %s, %s, %s)"
        self.cursor.execute(sql, (new_id, name, email, phone, address, today))
        self.conn.commit()
        return new_id
    
    def delete_user(self, id):
        """Xóa user theo ID"""
        self.cursor.execute("DELETE FROM customers WHERE id = %s", (id,))
        self.conn.commit()
        
    def update_user(self, id, name, email, phone, address, created_at):
        """Updates a customer in the database."""
        sql = "UPDATE customers SET name=%s, email=%s, phone=%s, address=%s, created_at=%s WHERE id=%s"
        self.cursor.execute(sql, (name, email, phone, address, created_at, id))
        self.conn.commit()
    def close(self):
        self.conn.close()