from DAO.TaiKhoanDAO import TaiKhoanDAO
import re

class TaiKhoanBUS:
    def __init__(self):
        self.DAO = TaiKhoanDAO()
    
    def get_user(self, username):
        user = self.DAO.get_user(username)
        if user is None:
            print(f"Warning: User '{username}' not found.")
        return self.DAO.get_user(username)
    def validate_login(self, username, password):
        """Validate user login"""
        return self.DAO.validate_login(username, password)
    def get_all(self):
        """Lấy danh sách tài khoản từ DAO"""
        return self.DAO.get_all()
    
    def insert_user(self, username, password, role, khachhang_id=None, nhanvien_id=None):
        # Validate username (should not be empty and must be at least 3 characters)
        if not username or len(username) < 3:
            raise ValueError("Username must be at least 3 characters long")
        
        # Validate password (should be at least 6 characters)
        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters long")
        
        # Ensure nhanvien_id exist
        if (self.NhanVienBUS.get_nhanvien(nhanvien_id) is None):
            raise ValueError("NhanVien ID does not exist")
        
        # If validation passes, proceed to insert the user
        new_user_id = self.DAO.insert_user(username, password, nhanvien_id)
        return new_user_id
    
    def close(self):
        self.DAO.close()
