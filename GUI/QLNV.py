from BUS.NhanVienBUS import NhanVienBUS
from PyQt6.QtCore import QDate
from PyQt6 import uic
from datetime import datetime
from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox

class QuanLyNhanVien(QMainWindow):
    def __init__(self):
        super().__init__()
        self.NhanVienBUS = NhanVienBUS()
        uic.loadUi("./GUI/QuanLyNhanVien.ui", self)
        self.load_data()

        # Connect row selection signal
        self.List.cellClicked.connect(self.fill_fields)

        # Connect buttons to functions
        self.btnEdit.clicked.connect(self.update_employee)
        self.btnAdd.clicked.connect(self.add_employee)
        self.btnDel.clicked.connect(self.delete_employee)
        self.btnReset.clicked.connect(self.reset_employee)
        self.btnKH.clicked.connect(self.open_customer_ui)
        self.btnHD.clicked.connect(self.open_reciept_ui)
        self.searchbutton.clicked.connect(self.search_employee)
    def load_data(self):
        """Load employee data into the table."""
        self.List.setRowCount(0)  # Clear table before loading new data
        employees = self.NhanVienBUS.get_all()
        
        for row_index, employee in enumerate(employees):
            self.List.insertRow(row_index)
            self.List.setItem(row_index, 0, QTableWidgetItem(str(employee.id)))
            self.List.setItem(row_index, 1, QTableWidgetItem(employee.name))
            self.List.setItem(row_index, 2, QTableWidgetItem(employee.email))
            self.List.setItem(row_index, 3, QTableWidgetItem(employee.password))
            self.List.setItem(row_index, 4, QTableWidgetItem(employee.role.value))  # Convert Enum to string before setting
            self.List.setItem(row_index, 5, QTableWidgetItem(str(employee.created_at)))
    def reset_employee(self):
        self.maNV.clear()
        self.tenNV.clear()
        self.email.clear()
        self.password.clear()
        self.dateDK.clear()
    def fill_fields(self, row, column):
        """Fill input fields when a row is selected."""
        self.maNV.setText(self.List.item(row, 0).text())
        self.tenNV.setText(self.List.item(row, 1).text())
        self.email.setText(self.List.item(row, 2).text())
        self.password.setText(self.List.item(row, 3).text())
        self.role.setCurrentText(self.List.item(row, 4).text())

        # Convert date string to QDate before setting it
        date_str = self.List.item(row, 5).text()  # Assuming date format is YYYY-MM-DD
        date_obj = QDate.fromString(date_str, "yyyy-MM-dd")  # Convert string to QDate
        self.dateDK.setDate(date_obj)
        self.dateDK.setDate(date_obj)

    def add_employee(self):
        """Insert a new employee into the database."""
        name = self.tenNV.text().strip()
        email = self.email.text().strip()
        password = self.password.text().strip()
        role = self.role.currentText().strip()

        if not name or not email or not password or not role:
            QMessageBox.warning(self, "Lỗi", "Vui lòng điền đầy đủ thông tin khách hàng!")
            return

        try:
            new_id = self.NhanVienBUS.insert_user(name, email, password, role)
            QMessageBox.information(self, "Thành công", f"Đã thêm nhân viên mới với ID: {new_id}")
            self.load_data()  # Refresh table
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"{str(e)}")

    def update_employee(self):
        """Update employee data in the database."""
        MaNV = self.maNV.text().strip()
        name = self.tenNV.text().strip()
        email = self.email.text().strip()
        password = self.password.text().strip()
        role = self.role.currentText().strip() 
        dateDK = self.dateDK.text().strip()
        
        self.NhanVienBUS.update_user(MaNV, name, email, password, role, dateDK) 
        QMessageBox.information(self, "Thành công", "Thông tin nhân viên đã được cập nhật!")
        print(dateDK)
        self.load_data()

    def delete_employee(self):
        """Delete a employee from the database."""
        maNV = self.maNV.text().strip()
        if not maNV:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn nhân viên cần xóa!")
            return

        confirm = QMessageBox.question(self, "Xác nhận", "Bạn có chắc muốn xóa nhân viên này?",
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirm == QMessageBox.StandardButton.Yes:
            self.NhanVienBUS.delete_user(maNV)
            QMessageBox.information(self, "Thành công", "Nhân viên đã được xóa!")
            self.load_data()
        else:
            return
    def search_employee(self):
        """Search employee by name."""
        search_text = self.search.text().strip().lower()
        if not search_text:
            self.load_data()  # Reload all data if search is empty
            return

        employees = self.NhanVienBUS.get_all()
        filtered_employees = [c for c in employees if search_text in c.name.lower()]

        self.List.setRowCount(0)  # Clear table
        for row_index, employee in enumerate(filtered_employees):
            self.List.insertRow(row_index)
            self.List.setItem(row_index, 0, QTableWidgetItem(str(employee.id)))
            self.List.setItem(row_index, 1, QTableWidgetItem(employee.name))
            self.List.setItem(row_index, 2, QTableWidgetItem(employee.email))
            self.List.setItem(row_index, 3, QTableWidgetItem(employee.password))
            self.List.setItem(row_index, 4, QTableWidgetItem(employee.role.value)) 
            self.List.setItem(row_index, 5, QTableWidgetItem(str(employee.created_at)))
    def open_customer_ui(self):
        from GUI.QLKH import QuanLyKhachHang
        self.employee_window = QuanLyKhachHang()
        self.employee_window.show()
        self.close()

    def open_reciept_ui(self):
        from GUI.QLHD import QuanLyHoaDon
        self.employee_window = QuanLyHoaDon()
        self.employee_window.show()
        self.close()
