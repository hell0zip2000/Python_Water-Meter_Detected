# Business Logic Layer (BUS) - Kiểm tra và xử lý logic nghiệp vụ
from datetime import datetime
from DAO.NhanVienDAO import NhanVienDAO
from DTO.NhanVienDTO import Role
import re

class NhanVienBUS:
    def __init__(self):
        self.DAO = NhanVienDAO()

    def get_user(self, id): 
        return self.DAO.get_user(id)
    
    def get_all(self):
        return self.DAO.get_all()

    def check_user(self, name, email, password, role):
        """Kiểm tra tính hợp lệ của dữ liệu người dùng"""
        name = name.strip().title()
        if not all(part.isalpha() for part in name.split()):
            raise ValueError("Tên chỉ được chứa chữ cái và khoảng trắng!")

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email): 
            raise ValueError("Email không đúng định dạng!")

        if len(password) < 6:
            raise ValueError("Mật khẩu phải có ít nhất 6 ký tự!")

        try:
            role = Role(role)
        except ValueError:
            raise ValueError(f"Role không hợp lệ! Phải là một trong {[r.value for r in Role]}")

        return name, email, password, role

    def insert_user(self, name, email, password, role):
        """Thêm người dùng mới"""
        name, email, password, role = self.check_user(name, email, password, role)

        if self.DAO.email_exists(email):
            raise ValueError("Email đã tồn tại!")

        new_user_id = self.DAO.insert_user(name, email, password, role.value)
        return new_user_id
    
    def update_user(self, id, name, email, password, role, NgayDangKy):
        """Cập nhật thông tin người dùng"""
        name, email, password, role = self.check_user(name, email, password, role)

        try:
            NgayDangKy = datetime.strptime(NgayDangKy, "%d/%m/%Y").strftime("%Y-%m-%d")
        except ValueError:
            raise ValueError("Ngày đăng ký không đúng định dạng 'DD/MM/YYYY'!")

        self.DAO.update_user(id, name, email, password, role.value, NgayDangKy)
    def delete_user(self, maNV):
        """Xóa người dùng theo mã nhân viên"""
        return self.DAO.delete_user(maNV)

    def validate_login(self, email, password):
        """Xác thực đăng nhập"""
        return self.DAO.validate_login(email, password)

    def close(self):
        self.DAO.close()
