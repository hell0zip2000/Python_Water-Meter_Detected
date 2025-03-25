from BUS.KhachHangBUS import KhachHangBUS
from PyQt6.QtCore import QDate
from PyQt6 import uic
from datetime import datetime
from GUI.QLHD import QuanLyHoaDon
from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox

class QuanLyKhachHang(QMainWindow):
    def __init__(self):
        super().__init__()
        self.KhachHangBUS = KhachHangBUS()
        uic.loadUi("./GUI/QuanLyKhachHang.ui", self)
        self.load_data()

        # Connect row selection signal
        self.List.cellClicked.connect(self.fill_fields)
        # Connect buttons to functions
        self.btnEdit.clicked.connect(self.update_customer)
        self.btnAdd.clicked.connect(self.add_customer)
        self.btnDel.clicked.connect(self.delete_customer)
        self.searchbutton.clicked.connect(self.search_customer)
        self.btnNV.clicked.connect(self.open_employee_ui)
        self.btnHD.clicked.connect(self.open_reciept_ui)
    def load_data(self):
        """Load customer data into the table."""
        self.List.setRowCount(0)  # Clear table before loading new data
        customers = self.KhachHangBUS.get_all()
        
        for row_index, customer in enumerate(customers):
            self.List.insertRow(row_index)
            self.List.setItem(row_index, 0, QTableWidgetItem(str(customer.id)))
            self.List.setItem(row_index, 1, QTableWidgetItem(customer.name))
            self.List.setItem(row_index, 2, QTableWidgetItem(customer.email))
            self.List.setItem(row_index, 3, QTableWidgetItem(customer.phone))
            self.List.setItem(row_index, 4, QTableWidgetItem(customer.address)) 
            self.List.setItem(row_index, 5, QTableWidgetItem(str(customer.created_at)))

    def fill_fields(self, row, column):
        """Fill input fields when a row is selected."""
        self.maKH.setText(self.List.item(row, 0).text())
        self.tenKH.setText(self.List.item(row, 1).text())
        self.email.setText(self.List.item(row, 2).text())
        self.phone.setText(self.List.item(row, 3).text())
        self.address.setText(self.List.item(row, 4).text())

        # Convert date string to QDate before setting it
        date_str = self.List.item(row, 5).text()  # Assuming date format is YYYY-MM-DD
        date_obj = QDate.fromString(date_str, "yyyy-MM-dd")  # Convert string to QDate
        self.dateDK.setDate(date_obj)
        self.dateDK.setDate(date_obj)

    def add_customer(self):
        """Insert a new customer into the database."""
        name = self.tenKH.text().strip()
        email = self.email.text().strip()
        phone = self.phone.text().strip()
        address = self.address.text().strip()

        if not name or not email or not phone or not address:
            QMessageBox.warning(self, "Lỗi", "Vui lòng điền đầy đủ thông tin khách hàng!")
            return

        try:
            new_id = self.KhachHangBUS.insert_user(name, email, phone, address)
            QMessageBox.information(self, "Thành công", f"Đã thêm khách hàng mới với ID: {new_id}")
            self.load_data()  # Refresh table
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi thêm khách hàng: {str(e)}")

    def update_customer(self):
        """Update customer data in the database."""
        maKH = self.maKH.text().strip()
        name = self.tenKH.text().strip()
        email = self.email.text().strip()
        phone = self.phone.text().strip()
        address = self.address.text().strip() 
        dateDK = self.dateDK.text().strip()
        try:
            dateDK = datetime.strptime(dateDK, "%d-%b-%y").strftime("%Y-%m-%d")
        except ValueError:
            QMessageBox.warning(self, "Lỗi", "Ngày đăng ký không hợp lệ!")
            return

        if not maKH or not name or not email or not phone or not address or not dateDK:
            QMessageBox.warning(self, "Lỗi", "Vui lòng điền đầy đủ thông tin khách hàng!")
            return

        self.KhachHangBUS.update_user(maKH, name, email, phone, address, dateDK) 
        QMessageBox.information(self, "Thành công", "Thông tin khách hàng đã được cập nhật!")
        self.load_data()

    def delete_customer(self):
        """Delete a customer from the database."""
        maKH = self.maKH.text().strip()
        if not maKH:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn khách hàng cần xóa!")
            return

        confirm = QMessageBox.question(self, "Xác nhận", "Bạn có chắc muốn xóa khách hàng này?",
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirm == QMessageBox.StandardButton.Yes:
            self.KhachHangBUS.delete_user(maKH)
            QMessageBox.information(self, "Thành công", "Khách hàng đã được xóa!")
            self.load_data()
        else:
            return
    def search_customer(self):
        """Search customers by name."""
        search_text = self.search.text().strip().lower()
        if not search_text:
            self.load_data()  # Reload all data if search is empty
            return

        customers = self.KhachHangBUS.get_all()
        filtered_customers = [c for c in customers if search_text in c.name.lower()]

        self.List.setRowCount(0)  # Clear table
        for row_index, customer in enumerate(filtered_customers):
            self.List.insertRow(row_index)
            self.List.setItem(row_index, 0, QTableWidgetItem(str(customer.id)))
            self.List.setItem(row_index, 1, QTableWidgetItem(customer.name))
            self.List.setItem(row_index, 2, QTableWidgetItem(customer.email))
            self.List.setItem(row_index, 3, QTableWidgetItem(customer.phone))
            self.List.setItem(row_index, 4, QTableWidgetItem(customer.address)) 
            self.List.setItem(row_index, 5, QTableWidgetItem(str(customer.created_at)))
    def open_employee_ui(self):
        from GUI.QLNV import QuanLyNhanVien
        self.employee_window = QuanLyNhanVien()
        self.employee_window.show()
        self.close()

    def open_reciept_ui(self):
        self.reciept_window = QuanLyHoaDon()
        self.reciept_window.show()
        self.close()