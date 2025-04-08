from DAO.TinhTienNuocDAO import TinhTienNuocDAO
class TinhTienNuocBUS:
    def __init__(self):
        self.tinhTienNuocDAO = TinhTienNuocDAO()

    def getWaterMeterById(self, meter_id):
        return self.tinhTienNuocDAO.getWaterMeterById(meter_id)

    def close_connection(self):
        return self.tinhTienNuocDAO.close_connection()
