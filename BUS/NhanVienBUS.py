
#Business Logic Layer/Business Object check and apply bussiness rules to the passed data to check for any logic invalidation (i.e non existing email, password too short, etc.)
from DAO.NhanVienDAO import NhanVienDAO
from DTO.NhanVienDTO import Role
import re
class NhanVienBUS:
    def __init__(self):
        self.DAO = NhanVienDAO()

    def get_user(self, id): 
        return self.DAO.get_user(id)
    
    def get_all(self):
        """Lấy danh sách nhân viên từ DAO"""
        return self.DAO.get_all()
    
    def insert_user(self, name, email, password, role):
        # Example validation: check if email is in valid format
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email): #[^@]+ means "one or more characters that are not @(john,nguyen,gmail,com)" && \. means a literal dot. && @ means a literal @
            raise ValueError("Invalid email format")
        # Check if email already exists
        if self.DAO.email_exists(email):
            raise ValueError("Email already exists")
         # Check if role is valid
        try:
            role = Role(role)
        except ValueError:
            raise ValueError(f"Invalid role '{role}'. Must be one of {[r.value for r in Role]}")

        new_user_id = self.DAO.insert_user(name, email, password, role.value)
        return new_user_id
    
    def update_user(self, id, name, email, password, role, NgayDangKy):
        """Updates an existing customer."""
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email): #[^@]+ means "one or more characters that are not @(john,nguyen,gmail,com)" && \. means a literal dot. && @ means a literal @
            raise ValueError("Invalid email format")
        # Check if role is valid
        try:
            role = Role(role)
        except ValueError:
            raise ValueError(f"Invalid role '{role}'. Must be one of {[r.value for r in Role]}")
        self.DAO.update_user(id, name, email, password, role.value, NgayDangKy)

    def validate_login(self, email, password):
        """Validate user login"""
        return self.DAO.validate_login(email, password)
    def close(self):
        self.DAO.close()
