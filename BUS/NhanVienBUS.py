
#Business Logic Layer/Business Object check and apply bussiness rules to the passed data to check for any logic invalidation (i.e non existing email, password too short, etc.)
from DAO.NhanVienDAO import NhanVienDAO
import re
class NhanVienBUS:
    def __init__(self):
        self.DAO = NhanVienDAO()
    def get_user(self, MaNhanVien): 
        return self.DAO.get_user(MaNhanVien)
    def get_all(self):
        """Lấy danh sách nhân viên từ DAO"""
        return self.DAO.get_all()

    def insert_user(self, HoTen, DiaChi, SoDienThoai, Email):
        # Example validation: check if email is in valid format
        if not re.match(r"[^@]+@[^@]+\.[^@]+", Email): #[^@]+ means "one or more characters that are not @(john,nguyen,gmail,com)" && \. means a literal dot. && @ means a literal @
            raise ValueError("Invalid email format")
        # Additional validations can go here:
        # If validation passes, proceed to insert the user
        new_user_id = self.KhachHangDAO.insert_user(HoTen, DiaChi, SoDienThoai, Email)
        return new_user_id
    def update_user(self, MaNhanVien, HoTen, DiaChi, SoDienThoai, Email, NgayDangKy):
        """Updates an existing customer."""
        if not re.match(r"[^@]+@[^@]+\.[^@]+", Email): #[^@]+ means "one or more characters that are not @(john,nguyen,gmail,com)" && \. means a literal dot. && @ means a literal @
            raise ValueError("Invalid email format")
        self.DAO.update_user(MaNhanVien, HoTen, DiaChi, SoDienThoai, Email, NgayDangKy)
    def close(self):
        self.DAO.close()
