from Database.database import Database

class CustomerDAO:
    def __init__(self):
        self.db = Database()

    def getAllCustomers(self):
        """Lấy danh sách tất cả khách hàng."""
        query = "SELECT * FROM customers"
        return self.db.fetch_all(query)

    def searchCustomer(self, keyword, search_type):
        """Tìm kiếm khách hàng theo loại."""
        query_map = {
            "Họ Tên": "name",
            "Địa Chỉ": "address",
            "Số Điện Thoại": "phone",
            "Email": "email",
            "Mã KH": "id",
        }
        column = query_map.get(search_type, "name")  # Mặc định tìm theo Họ Tên
        
        query = f"SELECT * FROM customers WHERE {column} LIKE %s"
        return self.db.fetch_all(query, (f"%{keyword}%",))

    def close_connection(self):
        """Đóng kết nối database."""
        self.db.close()
