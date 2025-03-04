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
        self.cursor.execute("SELECT * FROM khachhang")
        rows = self.cursor.fetchall()
        for row in rows:
            user_dto = KhachHangDTO(row[0], row[1], row[2], row[3], row[4])  # Truyền đúng thứ tự
            listKH.append(user_dto)  # Thêm vào danh sách
        return listKH

    def get_user(self, MaKhachHang):
        """Lấy thông tin user theo ID"""
        self.cursor.execute("SELECT * FROM khachhang WHERE id = %s", (MaKhachHang,))
        row = self.cursor.fetchone()
        if row:
            return KhachHangDTO(row[0], row[1], row[2], row[3], row[4])  # Trả về đối tượng DTO
        return None

    def insert_user(self, HoTen, Email):
        """Thêm user mới"""
        self.cursor.execute("SELECT MAX(MaKhachHang) FROM khachhang")
        max_id = self.cursor.fetchone()[0]
        new_id = max_id + 1 if max_id is not None else 1

        sql = "INSERT INTO khachhang (MaKhachHang, HoTen, Email) VALUES (%s, %s, %s)"
        self.cursor.execute(sql, (new_id, HoTen, Email))
        self.conn.commit()
        return new_id

    def close(self):
        self.conn.close()