import os
from PyQt6 import QtWidgets  
from PyQt6.QtWidgets import QApplication, QMainWindow, QMenuBar, QMenu, QMessageBox, QTableWidget, QTableWidgetItem, QLineEdit
from PyQt6.QtGui import QAction
from PyQt6 import uic
from PyQt6.QtCore import QDate

from PyQt6.uic import loadUi
import sys
import MySQLdb as mdb

from GUI.NhanVien_GUI import NhanVien_GUI
from GUI.HoaDon_Gui import QuanLyHoaDon_w

class main_GUI(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('GUI/UI/main.ui', self)

        self.actionNV.triggered.connect(self.nhanVien_open) #nút action
        self.actionKH.triggered.connect(self.khachHang_open) 
        self.actionHD.triggered.connect(self.hoaDon_open)
        self.actionExit.triggered.connect(self.exit_app)
        
    def exit_app(self):
        QMessageBox.information(self, "Đăng xuất", "Đăng xuất thành công!")
        self.close() 
    def nhanVien_open(self):
        self.NhanVien_win = NhanVien_GUI(self) 
        self.NhanVien_win.show() 
        self.close()  

    def khachHang_open(self):
        QMessageBox.information(self, "Thông báo", "thành công!")
    def hoaDon_open(self):
        self.hoaDon_win = QuanLyHoaDon_w(self)
        self.hoaDon_win.show()
        self.close()
        
    


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_F = main_GUI()

    main_F.show()
    sys.exit(app.exec())
