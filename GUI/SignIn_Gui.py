
from PyQt6 import QtWidgets  
from PyQt6.QtWidgets import QApplication, QMainWindow, QMenuBar, QMenu, QMessageBox, QTableWidget, QTableWidgetItem, QLineEdit
from PyQt6.QtGui import QAction
from PyQt6 import uic
from PyQt6.QtCore import QDate

from PyQt6.uic import loadUi
import sys
import MySQLdb as mdb

class Reg_w(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('register.ui',self)
        self.btnReg.clicked.connect(self.reg)
    def reg(self):
        user = self.user.text()
        psw = self.txtPass.text()
        psw_again = self.txtPass_2.text()

        if psw != psw_again:
            QMessageBox.warning(self, "Đăng ký", "Mật khẩu nhập lại không trùng khớp")
            return

        try:
            db = mdb.connect(host="localhost", user="root", password="", database="donghonuoc")
            query = db.cursor()
            
            # Kiểm tra xem tài khoản đã tồn tại chưa
            query.execute(f"SELECT * FROM taikhoan WHERE username = '{user}'")
            kt = query.fetchone()

            if kt:
                QMessageBox.warning(self, "Đăng ký", "Tài khoản đã tồn tại")
            else:
                query.execute(f"INSERT INTO user_list (username, password) VALUES ('{user}', '{psw}')")
                db.commit()
                QMessageBox.information(self, "Đăng ký", "Tạo tài khoản thành công!")
                widget.setCurrentIndex(0)  # Quay lại màn hình login

            db.close()
        except mdb.Error as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi kết nối MySQL: {e}")