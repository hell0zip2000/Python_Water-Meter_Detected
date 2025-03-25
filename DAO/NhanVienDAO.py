# Data Access Object/ interact with SQL database with insert, delete, update. taken from DTO through BUS 
from Config.databaseConnect import get_conn
from DTO.NhanVienDTO import NhanVienDTO, Role  # Import lớp DTO
from datetime import datetime
class NhanVienDAO:
    def __init__(self):
        self.conn = get_conn()
        self.cursor = self.conn.cursor()

    def get_all(self):
        listKH = []
        """Lấy thông tin user theo ID"""
        self.cursor.execute("SELECT * FROM employees")
        rows = self.cursor.fetchall()
        for row in rows:
            user_dto = NhanVienDTO(row[0], row[1], row[2], row[3], row[4],row[5])  # transform useless tuples into DTO
            listKH.append(user_dto)  # Thêm vào danh sách
        return listKH

    def get_user(self, id):
        """Lấy thông tin user theo ID"""
        self.cursor.execute("SELECT * FROM employees WHERE id = %s", (id,))
        row = self.cursor.fetchone()
        if row:
            return NhanVienDTO(row[0], row[1], row[2], row[3], row[4])  # Trả về đối tượng DTO
        return None

    def insert_user(self, name, email, password, role):
        """Thêm user mới"""
        self.cursor.execute("SELECT MAX(id) FROM employees")
        max_id = self.cursor.fetchone()[0]
        new_id = max_id + 1 if max_id is not None else 1
        today = datetime.today().strftime('%Y-%m-%d')
        sql = "INSERT INTO employees (id, name, email, password, role, created_at) VALUES (%s, %s, %s, %s, %s, %s)"
        self.cursor.execute(sql, (new_id, name, email, password, role, today))
        self.conn.commit()
        return new_id
    
    def delete_user(self, id):
        """Xóa user theo ID"""
        self.cursor.execute("DELETE FROM employees WHERE id = %s", (id,))
        self.conn.commit()

    def update_user(self, id, name, email, password, role, created_at):
        """Updates a employee in the database."""
        sql = "UPDATE employees SET name=%s, email=%s, password=%s, role=%s, created_at=%s WHERE id=%s"
        self.cursor.execute(sql, (name, email, password, role, created_at, id))
        self.conn.commit()
        
    def validate_login(self, email, password):
        """Check if the provided email and password match a record in the database"""
        self.cursor.execute("SELECT password, role FROM employees WHERE email = %s", (email,))
        row = self.cursor.fetchone()
        
        if not row:
            return False, "Email not found.", None
        
        stored_password, role_str = row  # Extract stored password and role
        
        if stored_password != password:
            return False, "Incorrect password.", None  # Return false if password is incorrect
        
        try:
            role = Role(role_str)  # Convert role string to Role enum
        except ValueError:
            return False, "Invalid role.", None
        
        self.cursor.execute("SELECT name FROM employees WHERE email = %s", (email,))
        row = self.cursor.fetchone()
        name = row[0]
        return True, f"Login successful, welcome {name}", role  # Return true on success

    def email_exists(self, email):
        """Check if an email already exists in the database."""
        query = "SELECT COUNT(*) FROM employees WHERE email = %s"
        self.cursor.execute(query, (email,))
        count = self.cursor.fetchone()[0]
        return count > 0

    def close(self):
        self.conn.close()