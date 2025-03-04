# Data Transfer Object, take in data and structure it to be passed on.
class KhachHangDTO:
    def __init__(self, MaKhachHang, HoTen, DiaChi, SoDienThoai, Email):
        self.MaKhachHang = MaKhachHang
        self.HoTen = HoTen
        self.DiaChi = DiaChi
        self.SoDienThoai = SoDienThoai
        self.Email = Email