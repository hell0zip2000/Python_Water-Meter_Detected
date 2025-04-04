from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem, QAbstractItemView, QHeaderView
from PyQt6.QtCore import Qt
#? Load giao diện sử dụng uic
from PyQt6 import uic
from BUS.CustomerBUS import CustomerBUS
from GUI.TinhTienNuoc import TinhTienNuoc

class ChonKhachHang(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("GUI/UI/chonKhachHangUI.ui", self)

        self.customerBUS = CustomerBUS()
        self.loadData()
        self.btnSubmit.clicked.connect(self.xacNhanKhachHang)
        self.btnClose.clicked.connect(self.close)
        self.txtSearch.textChanged.connect(self.timKiemKhachHang)

    def loadData(self):
        listCustomer = self.customerBUS.getAllCustomers()
        self.tbDanhSachKhachHang.setRowCount(len(listCustomer))
        self.tbDanhSachKhachHang.setColumnCount(5)
        self.tbDanhSachKhachHang.setHorizontalHeaderLabels(["Mã KH", "Họ tên", "Địa chỉ", "Số điện thoại", "Email"])
        self.tbDanhSachKhachHang.verticalHeader().setVisible(False)
        self.tbDanhSachKhachHang.setColumnWidth(0, 100)
        for col in range(1, 6):
            self.tbDanhSachKhachHang.horizontalHeader().setSectionResizeMode(col, QHeaderView.ResizeMode.Stretch)

        # Chỉ cho phép chọn nguyên hàng
        self.tbDanhSachKhachHang.setSelectionBehavior(self.tbDanhSachKhachHang.SelectionBehavior.SelectRows)
        self.tbDanhSachKhachHang.setSelectionMode(self.tbDanhSachKhachHang.SelectionMode.SingleSelection)


        for row, customer in enumerate(listCustomer):
            item_id = QTableWidgetItem(str(customer["id"]))
            item_id.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.tbDanhSachKhachHang.setItem(row, 0, item_id)
            self.tbDanhSachKhachHang.setItem(row, 1, QTableWidgetItem(customer["name"]))
            self.tbDanhSachKhachHang.setItem(row, 2, QTableWidgetItem(customer["address"]))
            self.tbDanhSachKhachHang.setItem(row, 3, QTableWidgetItem(customer["phone"]))
            self.tbDanhSachKhachHang.setItem(row, 4, QTableWidgetItem(customer["email"]))

    def xacNhanKhachHang(self):
        selected_row = self.tbDanhSachKhachHang.currentRow()
        if selected_row == -1:
            return  # Không chọn khách nào

        data = {
            "id": self.tbDanhSachKhachHang.item(selected_row, 0).text(),
            "name": self.tbDanhSachKhachHang.item(selected_row, 1).text(),
            "address": self.tbDanhSachKhachHang.item(selected_row, 2).text(),
            "phone": self.tbDanhSachKhachHang.item(selected_row, 3).text(),
            "email": self.tbDanhSachKhachHang.item(selected_row, 4).text(),
        }

        self.tinhTienNuoc = TinhTienNuoc(data)
        self.tinhTienNuoc.show()
        self.close()
    def timKiemKhachHang(self):
        keyword = self.txtSearch.toPlainText().strip()
        search_type = self.cbTypeSearch.currentText()
        listCustomer = self.customerBUS.searchCustomer(keyword, search_type)
        self.tbDanhSachKhachHang.setRowCount(len(listCustomer))
        for row, customer in enumerate(listCustomer):
            item_id = QTableWidgetItem(str(customer["id"]))
            item_id.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.tbDanhSachKhachHang.setItem(row, 0, item_id)
            self.tbDanhSachKhachHang.setItem(row, 1, QTableWidgetItem(customer["name"]))
            self.tbDanhSachKhachHang.setItem(row, 2, QTableWidgetItem(customer["address"]))
            self.tbDanhSachKhachHang.setItem(row, 3, QTableWidgetItem(customer["phone"]))
            self.tbDanhSachKhachHang.setItem(row, 4, QTableWidgetItem(customer["email"]))
