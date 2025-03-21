import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from PyQt6.QtWidgets import QApplication, QWidget, QMessageBox, QMainWindow, QPushButton, QLineEdit, QTableWidgetItem
from PyQt6.QtCore import QDate
from PyQt6 import uic
from datetime import datetime
from BUS.KhachHangBUS import KhachHangBUS
from BUS.TaiKhoanBUS import TaiKhoanBUS
from BUS.NhanVienBUS import NhanVienBUS
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
            self.List.setItem(row_index, 0, QTableWidgetItem(str(customer.MaKhachHang)))
            self.List.setItem(row_index, 1, QTableWidgetItem(customer.HoTen))
            self.List.setItem(row_index, 2, QTableWidgetItem(customer.DiaChi))
            self.List.setItem(row_index, 3, QTableWidgetItem(customer.SoDienThoai))
            self.List.setItem(row_index, 4, QTableWidgetItem(customer.Email)) 
            self.List.setItem(row_index, 5, QTableWidgetItem(str(customer.NgayDangKy)))

    def fill_fields(self, row, column):
        """Fill input fields when a row is selected."""
        self.maKH.setText(self.List.item(row, 0).text())
        self.tenKH.setText(self.List.item(row, 1).text())
        self.address.setText(self.List.item(row, 2).text())
        self.phone.setText(self.List.item(row, 3).text())
        self.email.setText(self.List.item(row, 4).text())

        # Convert date string to QDate before setting it
        date_str = self.List.item(row, 5).text()  # Assuming date format is YYYY-MM-DD
        date_obj = QDate.fromString(date_str, "yyyy-MM-dd")  # Convert string to QDate
        self.dateDK.setDate(date_obj)
        self.dateDK.setDate(date_obj)

    def add_customer(self):
        """Insert a new customer into the database."""
        HoTen = self.tenKH.text().strip()
        DiaChi = self.address.text().strip()
        SoDienThoai = self.phone.text().strip()
        Email = self.email.text().strip()

        if not HoTen or not DiaChi or not SoDienThoai or not Email:
            QMessageBox.warning(self, "Lỗi", "Vui lòng điền đầy đủ thông tin khách hàng!")
            return

        try:
            new_id = self.KhachHangBUS.insert_user(HoTen, DiaChi, SoDienThoai, Email)
            QMessageBox.information(self, "Thành công", f"Đã thêm khách hàng mới với ID: {new_id}")
            self.load_data()  # Refresh table
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi thêm khách hàng: {str(e)}")

    def update_customer(self):
        """Update customer data in the database."""
        maKH = self.maKH.text().strip()
        HoTen = self.tenKH.text().strip()
        DiaChi = self.address.text().strip()
        SoDienThoai = self.phone.text().strip()
        Email = self.email.text().strip() 
        dateDK = self.dateDK.text().strip()
        try:
            dateDK = datetime.strptime(dateDK, "%d-%b-%y").strftime("%Y-%m-%d")
        except ValueError:
            QMessageBox.warning(self, "Lỗi", "Ngày đăng ký không hợp lệ!")
            return

        if not maKH or not HoTen or not DiaChi or not SoDienThoai or not Email or not dateDK:
            QMessageBox.warning(self, "Lỗi", "Vui lòng điền đầy đủ thông tin khách hàng!")
            return

        self.KhachHangBUS.update_user(maKH, HoTen, DiaChi, SoDienThoai, Email, dateDK) 
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
        filtered_customers = [c for c in customers if search_text in c.HoTen.lower()]

        self.List.setRowCount(0)  # Clear table
        for row_index, customer in enumerate(filtered_customers):
            self.List.insertRow(row_index)
            self.List.setItem(row_index, 0, QTableWidgetItem(str(customer.MaKhachHang)))
            self.List.setItem(row_index, 1, QTableWidgetItem(customer.HoTen))
            self.List.setItem(row_index, 2, QTableWidgetItem(customer.DiaChi))
            self.List.setItem(row_index, 3, QTableWidgetItem(customer.SoDienThoai))
            self.List.setItem(row_index, 4, QTableWidgetItem(customer.Email)) 
            self.List.setItem(row_index, 5, QTableWidgetItem(str(customer.NgayDangKy)))
    def open_employee_ui(self):
        self.customer_window = QuanLyNhanVien()
        self.customer_window.show()
        self.close()

    def open_reciept_ui(self):
        self.customer_window = QuanLyHoaDon()
        self.customer_window.show()
        self.close()

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
        self.btnKH.clicked.connect(self.open_customer_ui)
        self.btnHD.clicked.connect(self.open_reciept_ui)
        self.searchbutton.clicked.connect(self.search_employee)
    def load_data(self):
        """Load customer data into the table."""
        self.List.setRowCount(0)  # Clear table before loading new data
        customers = self.NhanVienBUS.get_all()
        
        for row_index, customer in enumerate(customers):
            self.List.insertRow(row_index)
            self.List.setItem(row_index, 0, QTableWidgetItem(str(customer.MaNhanVien)))
            self.List.setItem(row_index, 1, QTableWidgetItem(customer.HoTen))
            self.List.setItem(row_index, 2, QTableWidgetItem(customer.DiaChi))
            self.List.setItem(row_index, 3, QTableWidgetItem(customer.SoDienThoai))
            self.List.setItem(row_index, 4, QTableWidgetItem(customer.Email)) 
            self.List.setItem(row_index, 5, QTableWidgetItem(str(customer.NgayVaoLam)))

    def fill_fields(self, row, column):
        """Fill input fields when a row is selected."""
        self.maNV.setText(self.List.item(row, 0).text())
        self.tenNV.setText(self.List.item(row, 1).text())
        self.address.setText(self.List.item(row, 2).text())
        self.phone.setText(self.List.item(row, 3).text())
        self.email.setText(self.List.item(row, 4).text())

        # Convert date string to QDate before setting it
        date_str = self.List.item(row, 5).text()  # Assuming date format is YYYY-MM-DD
        date_obj = QDate.fromString(date_str, "yyyy-MM-dd")  # Convert string to QDate
        self.dateDK.setDate(date_obj)
        self.dateDK.setDate(date_obj)

    def add_employee(self):
        """Insert a new employee into the database."""
        HoTen = self.tenNV.text().strip()
        DiaChi = self.address.text().strip()
        SoDienThoai = self.phone.text().strip()
        Email = self.email.text().strip()

        if not HoTen or not DiaChi or not SoDienThoai or not Email:
            QMessageBox.warning(self, "Lỗi", "Vui lòng điền đầy đủ thông tin khách hàng!")
            return

        try:
            new_id = self.NhanVienBUS.insert_user(HoTen, DiaChi, SoDienThoai, Email)
            QMessageBox.information(self, "Thành công", f"Đã thêm nhân viên mới với ID: {new_id}")
            self.load_data()  # Refresh table
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi thêm nhân viên: {str(e)}")

    def update_employee(self):
        """Update employee data in the database."""
        MaNV = self.maNV.text().strip()
        HoTen = self.tenNV.text().strip()
        DiaChi = self.address.text().strip()
        SoDienThoai = self.phone.text().strip()
        Email = self.email.text().strip() 
        dateDK = self.dateDK.text().strip()
        try:
            dateDK = datetime.strptime(dateDK, "%d-%b-%y").strftime("%Y-%m-%d")
        except ValueError:
            QMessageBox.warning(self, "Lỗi", "Ngày đăng ký không hợp lệ!")
            return

        if not MaNV or not HoTen or not DiaChi or not SoDienThoai or not Email or not dateDK:
            QMessageBox.warning(self, "Lỗi", "Vui lòng điền đầy đủ thông tin khách hàng!")
            return

        self.NhanVienBUS.update_user(MaNV, HoTen, DiaChi, SoDienThoai, Email, dateDK) 
        QMessageBox.information(self, "Thành công", "Thông tin nhân viên đã được cập nhật!")
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
        filtered_employees = [c for c in employees if search_text in c.HoTen.lower()]

        self.List.setRowCount(0)  # Clear table
        for row_index, customer in enumerate(filtered_employees):
            self.List.insertRow(row_index)
            self.List.setItem(row_index, 0, QTableWidgetItem(str(customer.MaNhanVien)))
            self.List.setItem(row_index, 1, QTableWidgetItem(customer.HoTen))
            self.List.setItem(row_index, 2, QTableWidgetItem(customer.DiaChi))
            self.List.setItem(row_index, 3, QTableWidgetItem(customer.SoDienThoai))
            self.List.setItem(row_index, 4, QTableWidgetItem(customer.Email)) 
            self.List.setItem(row_index, 5, QTableWidgetItem(str(customer.NgayVaoLam)))
    def open_customer_ui(self):
        self.customer_window = QuanLyKhachHang()
        self.customer_window.show()
        self.close()

    def open_reciept_ui(self):
        self.customer_window = QuanLyHoaDon()
        self.customer_window.show()
        self.close()

class QuanLyHoaDon(QMainWindow):
    def __init__(self):
        super().__init__()
        self.NhanVienBUS = NhanVienBUS()
        uic.loadUi("./GUI/QuanLyHoaDon.ui", self)
        #self.load_data()
        self.btnKH.clicked.connect(self.open_customer_ui)
        self.btnNV.clicked.connect(self.open_employee_ui)

    def open_customer_ui(self):
        self.customer_window = QuanLyKhachHang()
        self.customer_window.show()
        self.close()
    
    def open_employee_ui(self):
        self.customer_window = QuanLyNhanVien()
        self.customer_window.show()
        self.close()

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("./GUI/Login.ui", self)  # Load UI file
        self.UserName = self.findChild(QLineEdit, "UserName") #find user name
        self.UserPassword = self.findChild(QLineEdit, "UserPassword") #find user password
        self.myButton = self.findChild(QPushButton, "LoginButton")  # Find login button
        self.myButton.clicked.connect(self.login)  # Remember to pass the definition/method, not the return value!
        self.show()
    def login(self):
        if(self.UserName.text() == "" or self.UserPassword.text() == ""):
            QMessageBox.warning(self, "Warning", "Please fill in all fields.")
            return
        else:
            taiKhoanBUS = TaiKhoanBUS()
            result, message = taiKhoanBUS.validate_login(self.UserName.text(), self.UserPassword.text())
            if result:
                QMessageBox.information(self, "login as employee", message)  
                self.open_manager_ui()
            else:
                QMessageBox.warning(self, "Warning", message)
            taiKhoanBUS.close()
    def open_manager_ui(self):
        """Open customer management UI and close login window"""
        self.customer_window = QuanLyKhachHang()
        self.customer_window.show()
        self.close()  # Close login window