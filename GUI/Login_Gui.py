from PyQt6.QtWidgets import QMainWindow, QMessageBox
from PyQt6.uic import loadUi
from BUS.LoginBUS import LoginBUS
from GUI.main_GUI import main_GUI  

class Login_w(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('GUI/UI/login.ui', self) 

        self.login_bus = LoginBUS()  
        self.btnLogin.clicked.connect(self.handle_login)

    def handle_login(self):
        username = self.user.text()
        password = self.txtPass.text()

        if self.login_bus.check_login(username, password):
            QMessageBox.information(self, "Thành công", "Đăng nhập thành công!")
            self.open_nhanvien_window()  
        else:
            QMessageBox.warning(self, "Lỗi", "Tên đăng nhập hoặc mật khẩu không đúng!")

    def open_nhanvien_window(self):
        self.main_window = main_GUI() 
        self.main_window.show()
        self.close()  
