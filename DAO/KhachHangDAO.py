# Data Access Object/ interact with SQL database with insert, delete, update. taken from DTO through BUS 
from Config.databaseConnect import conn
from DTO.KhachHangDTO import KhachHangDTO  # Import lớp DTO
from datetime import datetime
class KhachHangDAO:
    def __init__(self):
        self.conn = conn
        self.cursor = self.conn.cursor()

    def get_all(self):
        listKH = []
        """Lấy thông tin user theo ID"""
        self.cursor.execute("SELECT * FROM khachhang")
        rows = self.cursor.fetchall()
        for row in rows:
            user_dto = KhachHangDTO(row[0], row[1], row[2], row[3], row[4])  # transform useless tuples into DTO
            listKH.append(user_dto)  # Thêm vào danh sách
        return listKH

    def get_user(self, MaKhachHang):
        """Lấy thông tin user theo ID"""
        self.cursor.execute("SELECT * FROM khachhang WHERE MaKhachHang = %s", (MaKhachHang,))
        row = self.cursor.fetchone()
        if row:
            return KhachHangDTO(row[0], row[1], row[2], row[3], row[4])  # Trả về đối tượng DTO
        return None

    def insert_user(self, HoTen, DiaChi, SoDienThoai, Email):
        """Thêm user mới"""
        self.cursor.execute("SELECT MAX(MaKhachHang) FROM khachhang")
        max_id = self.cursor.fetchone()[0]
        new_id = max_id + 1 if max_id is not None else 1
        today = datetime.today().strftime('%Y-%m-%d')
        sql = "INSERT INTO khachhang (MaKhachHang, HoTen, DiaChi, SoDienThoai, Email, NgayDangKy) VALUES (%s, %s, %s, %s, %s, %s)"
        self.cursor.execute(sql, (new_id, HoTen, DiaChi, SoDienThoai, Email, today))
        self.conn.commit()
        return new_id

    def close(self):
        self.conn.close()