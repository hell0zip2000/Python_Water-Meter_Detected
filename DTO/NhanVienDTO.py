# Data Transfer Object, take in data and structure it to be passed on.
class NhanVienDTO:
    def __init__(self, MaNhanVien, HoTen, DiaChi, SoDienThoai, Email, NgayVaoLam):
        self.MaNhanVien = MaNhanVien
        self.HoTen = HoTen
        self.DiaChi = DiaChi
        self.SoDienThoai = SoDienThoai
        self.Email = Email
        self.NgayVaoLam = NgayVaoLam
    def __str__(self):
        return f"{self.MaKhachHang} - {self.HoTen} - {self.DiaChi} - {self.SoDienThoai} - {self.Email} - {self.NgayVaoLam}"