# Data Access Object (DAO) for interacting with the 'taikhoan' table
from Config.databaseConnect import get_conn
from DTO.TaiKhoanDTO import TaiKhoanDTO  # Import DTO

class TaiKhoanDAO:
    def __init__(self):
        self.conn = get_conn()
        self.cursor = self.conn.cursor()

    def get_all(self):
        """Retrieve all user accounts from the 'taikhoan' table"""
        list_accounts = []
        self.cursor.execute("SELECT * FROM taikhoan")
        rows = self.cursor.fetchall()
        for row in rows:
            account_dto = TaiKhoanDTO(row[0], row[1], row[2], row[3])  
            list_accounts.append(account_dto)  
        return list_accounts

    def get_user(self, username):
        """Retrieve user account by username"""
        self.cursor.execute("SELECT * FROM taikhoan WHERE username = %s", (username,))
        row = self.cursor.fetchone()
        if row:
            return TaiKhoanDTO(row[0], row[1], row[2], row[3])
        return None
    def validate_login(self, username, password):
        """Check if the provided username and password match a record in the database"""
        self.cursor.execute("SELECT password FROM taikhoan WHERE username = %s", (username,))
        row = self.cursor.fetchone()
    
        stored_password = row[0]  # Extract stored password
    
        if stored_password != password:
            return False, "Incorrect password."  # Return false if password is incorrect
    
        return True, f"Login successful, welcome {username}"  # Return true on success
    def insert_user(self, username, password, nhanvien_id):
        """Insert a new user account"""
        self.cursor.execute("SELECT MAX(id) FROM taikhoan")
        max_id = self.cursor.fetchone()[0]
        new_id = max_id + 1 if max_id is not None else 1
        
        sql = """
        INSERT INTO taikhoan (id, username, password, nhanvien_id) 
        VALUES (%s, %s, %s, %s)
        """
        self.cursor.execute(sql, (new_id, username, password, nhanvien_id))
        self.conn.commit()
        return new_id  # Return the ID of the newly inserted user

    def close(self):
        """Close database connection"""
        self.conn.close()
