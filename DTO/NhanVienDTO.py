from enum import Enum

class Role(Enum):
    ADMIN = "ADMIN"
    STAFF = "STAFF"

class NhanVienDTO:
    def __init__(self, id, name, email, password, role, created_at):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        try:
            self.role = Role(role)  # Ensures valid role
        except ValueError:
            raise ValueError(f"Invalid role '{role}'. Must be one of {[r.value for r in Role]}")
        self.created_at = created_at

    def __str__(self):
        return f"{self.id} - {self.name} - {self.email} - {self.password} - {self.role.value} - {self.created_at}"