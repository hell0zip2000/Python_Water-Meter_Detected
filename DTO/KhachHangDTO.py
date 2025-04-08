# Data Transfer Object, take in data and structure it to be passed on.
class KhachHangDTO:
    def __init__(self, id, name, email, phone, address, created_at):
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address        
        self.created_at = created_at
    def __str__(self):
        return f"{self.id} - {self.name} - {self.email} - {self.phone} - {self.address} - {self.created_at}"
