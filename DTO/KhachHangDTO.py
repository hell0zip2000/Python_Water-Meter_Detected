# Data Transfer Object, take in data and structure it to be passed on.
class KhachHangDTO:
    def __init__(self, MaKhachHang, HoTen, DiaChi, SoDienThoai, Email, NgayDangKy):
        self.MaKhachHang = MaKhachHang
        self.HoTen = HoTen
        self.DiaChi = DiaChi
        self.SoDienThoai = SoDienThoai
        self.Email = Email
        self.NgayDangKy = NgayDangKy
    def __str__(self):
        return f"{self.MaKhachHang} - {self.HoTen} - {self.DiaChi} - {self.SoDienThoai} - {self.Email} - {self.NgayDangKy}"