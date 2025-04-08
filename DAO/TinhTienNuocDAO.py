from Database.database import Database

class TinhTienNuocDAO:
    def __init__(self):
        self.db = Database()

    def getWaterMeterById(self, meter_id):
        """Lấy thông tin đồng hồ nước theo mã."""
        query = "SELECT * FROM water_meters WHERE id = %s"
        result = self.db.fetch_all(query, (meter_id,))
        if result:
            return result[0]
        return

    def close_connection(self):
        """Đóng kết nối database."""
        self.db.close()
