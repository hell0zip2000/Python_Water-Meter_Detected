# Data Access Object/ interact with SQL database with insert, delete, update. taken from DTO through BUS 
from Config.databaseConnect import get_conn
from DTO.NhanVienDTO import NhanVienDTO  # Import lớp DTO
from datetime import datetime
class NhanVienDAO:
    def __init__(self):
        self.conn = get_conn()
        self.cursor = self.conn.cursor()

    def get_all(self):
        listKH = []
        """Lấy thông tin user theo ID"""
        self.cursor.execute("SELECT * FROM NhanVien")
        rows = self.cursor.fetchall()
        for row in rows:
            user_dto = NhanVienDTO(row[0], row[1], row[2], row[3], row[4],row[5])  # transform useless tuples into DTO
            listKH.append(user_dto)  # Thêm vào danh sách
        return listKH

    def get_user(self, MaNhanVien):
        """Lấy thông tin user theo ID"""
        self.cursor.execute("SELECT * FROM nhanvien WHERE MaNhanVien = %s", (MaNhanVien,))
        row = self.cursor.fetchone()
        if row:
            return NhanVienDTO(row[0], row[1], row[2], row[3], row[4])  # Trả về đối tượng DTO
        return None

    def insert_user(self, HoTen, DiaChi, SoDienThoai, Email):
        """Thêm user mới"""
        self.cursor.execute("SELECT MAX(MaNhanVien) FROM nhanvien")
        max_id = self.cursor.fetchone()[0]
        new_id = max_id + 1 if max_id is not None else 1
        today = datetime.today().strftime('%Y-%m-%d')
        sql = "INSERT INTO NhanVien (MaNhanVien, HoTen, DiaChi, SoDienThoai, Email, NgayVaoLam) VALUES (%s, %s, %s, %s, %s, %s)"
        self.cursor.execute(sql, (new_id, HoTen, DiaChi, SoDienThoai, Email, today))
        self.conn.commit()
        return new_id
    def update_user(self, MaNhanVien, HoTen, DiaChi, SoDienThoai, Email, NgayDangKy):
        """Updates a employee in the database."""
        sql = "UPDATE NhanVien SET HoTen=%s, DiaChi=%s, SoDienThoai=%s, Email=%s, NgayVaoLam=%s WHERE MaNhanVien=%s"
        self.cursor.execute(sql, (HoTen, DiaChi, SoDienThoai, Email, NgayDangKy, MaNhanVien))
        self.conn.commit()
    def close(self):
        self.conn.close()