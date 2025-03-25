class TaiKhoanDTO:
    def __init__(self, id, username, password, nhanvien_id=None):
        self.id = id
        self.username = username
        self.password = password
        self.nhanvien_id = nhanvien_id

    def __str__(self):
        return f"id={self.id}, username={self.username}, password={self.password} nhanvien_id={self.nhanvien_id}"
