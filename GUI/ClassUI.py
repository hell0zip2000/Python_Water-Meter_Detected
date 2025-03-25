import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from PyQt6.QtWidgets import QApplication, QWidget, QMessageBox, QMainWindow, QPushButton, QLineEdit, QTableWidgetItem
from PyQt6.QtCore import QDate
from PyQt6 import uic
from datetime import datetime
from BUS.KhachHangBUS import KhachHangBUS
from BUS.NhanVienBUS import NhanVienBUS
from DTO.NhanVienDTO import Role
from GUI.QLKH import QuanLyKhachHang

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("./GUI/Login.ui", self)  # Load UI file
        self.UserEmail = self.findChild(QLineEdit, "UserEmail") #find email
        self.UserPassword = self.findChild(QLineEdit, "UserPassword") #find user password
        self.myButton = self.findChild(QPushButton, "LoginButton")  # Find login button
        self.myButton.clicked.connect(self.login)  # Remember to pass the definition/method, not the return value!
        self.show()
    def login(self):
        if(self.UserEmail.text() == "" or self.UserPassword.text() == ""):
            QMessageBox.warning(self, "Warning", "Please fill in all fields.")
            return
        else:
            self.NhanVienBUS = NhanVienBUS()
            result, message, role = self.NhanVienBUS.validate_login(self.UserEmail.text(), self.UserPassword.text())
            if result:
                if role == Role.ADMIN:
                    QMessageBox.information(self, "Login as Admin", message)
                    self.open_manager_ui()
                elif role == Role.STAFF:
                    QMessageBox.information(self, "Login as Staff", message)
                    self.open_employee_ui()
                else:
                    QMessageBox.warning(self, "Warning", "Invalid role taken from database.")
            else:
                QMessageBox.warning(self, "Warning", message)
            self.NhanVienBUS.close()
    def open_manager_ui(self):
        """Open customer management UI and close login window"""
        self.customer_window = QuanLyKhachHang()
        self.customer_window.show()
        self.close()  # Close login window