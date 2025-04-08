from Config.databaseConnect import DatabaseConnect
from DTO.NhanVienDTO import NhanVienDTO

import MySQLdb

class NhanVienDAO:
    def __init__(self):
        self.db = DatabaseConnect()  

    def get_all_nhanvien(self):
        query = "SELECT maNV, hoTen, chucVu, soDienThoai, email, ngayVaoLam FROM nhanvien"
        data = self.db.fetch_all(query)
        
        print(f"🔍 Kết quả truy vấn từ DB: {data}")  # Debug dữ liệu

        return [NhanVienDTO(**row) for row in data] if data else []


    def insert(self, nhanvien: NhanVienDTO):
        query = """
        INSERT INTO nhanvien (maNV, hoTen, chucVu, soDienThoai, email, ngayVaoLam) 
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (nhanvien.maNV, nhanvien.hoTen, nhanvien.chucVu, nhanvien.soDienThoai, nhanvien.email, nhanvien.ngayVaoLam)
        try:
            return self.db.execute(query, params)
        except MySQLdb.Error as e:
            print(f"Lỗi khi thêm nhân viên: {e}")
            return False

    def delete(self, maNV):
        try:
            # Xóa tất cả dữ liệu liên quan trong bảng hinhanhdongho trước
            self.db.cursor.execute("DELETE FROM hinhanhdongho WHERE MaChiSo IN (SELECT MaChiSo FROM chisodongho WHERE MaNhanVien = %s)", (maNV,))
            self.db.conn.commit()
            print("Đã xóa dữ liệu liên quan trong hinhanhdongho!")

            # Xóa dữ liệu trong bảng chisodongho
            self.db.cursor.execute("DELETE FROM chisodongho WHERE MaNhanVien = %s", (maNV,))
            self.db.conn.commit()
            print("Đã xóa dữ liệu liên quan trong chisodongho!")

            # Xóa nhân viên trong bảng nhanvien
            self.db.cursor.execute("DELETE FROM nhanvien WHERE maNV = %s", (maNV,))
            self.db.conn.commit()
            print("Xóa nhân viên thành công!")

            return True
        except Exception as e:
            print(f"Lỗi khi xóa: {e}")
            return False




    def update(self, nhanvien: NhanVienDTO):
        query = """
        UPDATE nhanvien SET hoTen=%s, chucVu=%s, soDienThoai=%s, email=%s, ngayVaoLam=%s 
        WHERE maNV=%s
        """
        params = (nhanvien.hoTen, nhanvien.chucVu, nhanvien.soDienThoai, nhanvien.email, nhanvien.ngayVaoLam, nhanvien.maNV)
        try:
            return self.db.execute(query, params)
        except MySQLdb.Error as e:
            print(f"Lỗi khi cập nhật nhân viên: {e}")
            return False
