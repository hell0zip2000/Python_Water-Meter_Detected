# Data Transfer Object, take in data and structure it to be passed on.
class KhachHangDTO:
    def __init__(self, KHID, HoTen, Email, phone, address):
        self.KHID = KHID
        self.HoTen = HoTen
        self.Email = Email
        self.phone = phone
        self.address = address