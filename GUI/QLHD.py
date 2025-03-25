from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox
from PyQt6 import uic

class QuanLyHoaDon(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("./GUI/QuanLyHoaDon.ui", self)
        #self.load_data()
        self.btnKH.clicked.connect(self.open_customer_ui)
        self.btnNV.clicked.connect(self.open_employee_ui)

    def open_customer_ui(self):
        from GUI.QLKH import QuanLyKhachHang
        self.customer_window = QuanLyKhachHang()
        self.customer_window.show()
        self.close()
    
    def open_employee_ui(self):
        from GUI.QLNV import QuanLyNhanVien
        self.employee_window = QuanLyNhanVien()
        self.employee_window.show()
        self.close()
