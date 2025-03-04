# Data Access Object/ interact with SQL database with insert, delete, update. taken from DTO through BUS 
from Config.databaseConnect import get_connection
from DTO.KhachHangDTO import KhachHangDTO  # Import lớp DTO

class KhachHangDAO:
    def __init__(self):
        self.conn = get_connection()  
        self.cursor = self.conn.cursor()

    def get_all(self):
        listKH = []
        """Lấy thông tin user theo ID"""
        self.cursor.execute("SELECT * FROM taikhoan")
        rows = self.cursor.fetchall()
        for row in rows:
            user_dto = KhachHangDTO(row[0], row[1], row[2], row[3], row[4])  # Truyền đúng thứ tự
            listKH.append(user_dto)  # Thêm vào danh sách
        return listKH

    def get_user(self, KHID):
        """Lấy thông tin user theo ID"""
        self.cursor.execute("SELECT * FROM taikhoan WHERE id = %s", (KHID,))
        row = self.cursor.fetchone()
        if row:
            return KhachHangDTO(row[0], row[1], row[2], row[3], row[4])  # Trả về đối tượng DTO
        return None

    def insert_user(self, HoTen, Email):
        """Thêm user mới"""
        sql = "INSERT INTO users (HoTen, Email) VALUES (%s, %s)"
        self.cursor.execute(sql, (HoTen, Email))
        self.conn.commit()
        return self.cursor.lastrowid

    def close(self):
        self.conn.close()