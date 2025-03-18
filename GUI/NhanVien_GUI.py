from PyQt6.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem
from PyQt6 import uic
import sys
from PyQt6.QtWidgets import QApplication, QStackedWidget
import os
from PyQt6 import QtWidgets  
from PyQt6.QtWidgets import QApplication, QMainWindow, QMenuBar, QMenu, QMessageBox, QTableWidget, QTableWidgetItem, QLineEdit
from PyQt6.QtGui import QAction
from PyQt6 import uic
from PyQt6.QtCore import QDate
from BUS.NhanVienBUS import NhanVienBUS 


class NhanVien_GUI(QMainWindow):
    def __init__(self, main_GUI):
        super().__init__()
        uic.loadUi('GUI/UI/QuanLyNhanVien.ui', self)

        self.main_window = main_GUI 
        self.nhanvien_bus = NhanVienBUS()  

        self.btnExit.clicked.connect(self.exit)
        self.btnAdd.clicked.connect(self.add_nhanvien)
        self.btnEdit.clicked.connect(self.update_nhanvien)
        self.btnDel.clicked.connect(self.delete_nhanvien)
        self.btnSearch.clicked.connect(self.search_nhanvien)
        self.btnReset.clicked.connect(self.reset)

        self.load_data()
        self.tableNhanVien.itemSelectionChanged.connect(self.load_selected_nhanvien)

    def load_data(self, filter_text=""):
        self.tableNhanVien.setRowCount(0)
        
        nhanvien_list = self.nhanvien_bus.get_all_nhanvien()
        
        for nhanvien in nhanvien_list:
            if filter_text and filter_text.lower() not in nhanvien.hoTen.lower():
                continue
            
            row = self.tableNhanVien.rowCount()
            self.tableNhanVien.insertRow(row)
            
            self.tableNhanVien.setItem(row, 0, QTableWidgetItem(str(nhanvien.maNV)))
            self.tableNhanVien.setItem(row, 1, QTableWidgetItem(nhanvien.hoTen))
            self.tableNhanVien.setItem(row, 2, QTableWidgetItem(nhanvien.chucVu))
            self.tableNhanVien.setItem(row, 3, QTableWidgetItem(nhanvien.soDienThoai))
            self.tableNhanVien.setItem(row, 4, QTableWidgetItem(nhanvien.email))
            
            ngayVaoLam_str = nhanvien.ngayVaoLam.strftime("%Y-%m-%d") if nhanvien.ngayVaoLam else ""
            self.tableNhanVien.setItem(row, 5, QTableWidgetItem(ngayVaoLam_str))

    def add_nhanvien(self):
        maNV = self.maNV.text()
        hoTen = self.tenNV.text()
        chucVu = self.chucVu.text()
        soDienThoai = self.phone.text()
        Email = self.txtEmail.text()
        NgayVaoLam = self.txtNgayVaoLam.date().toPyDate()  

        self.nhanvien_bus.add_nhanvien(maNV, hoTen, chucVu, soDienThoai, Email, NgayVaoLam)

        self.load_data() 
    def load_selected_nhanvien(self):
        selected_row = self.tableNhanVien.currentRow()
        if selected_row == -1:
            return 

        def get_item_text(row, col):
                item = self.tableNhanVien.item(row, col)
                return item.text() if item is not None else ""  

        self.maNV.setText(get_item_text(selected_row, 0))
        self.tenNV.setText(get_item_text(selected_row, 1))
        self.chucVu.setText(get_item_text(selected_row, 2))
        self.phone.setText(get_item_text(selected_row, 3))
        self.txtEmail.setText(get_item_text(selected_row, 4))  

        ngay_vao_lam_str = get_item_text(selected_row, 5)
        if ngay_vao_lam_str: 
            ngay_vao_lam = QDate.fromString(ngay_vao_lam_str, "yyyy-MM-dd")  
            self.txtNgayVaoLam.setDate(ngay_vao_lam)
        else:
            self.txtNgayVaoLam.clear()  


    def update_nhanvien(self):
        selected_row = self.tableNhanVien.currentRow()
        if selected_row == -1:  
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn một nhân viên để sửa!")
            return
    
        maNV = self.maNV.text()
        hoTen = self.tenNV.text()
        chucVu = self.chucVu.text()
        soDienThoai = self.phone.text()
        Email = self.txtEmail.text()
        NgayVaoLam = self.txtNgayVaoLam.date().toPyDate()

        self.nhanvien_bus.update_nhanvien(maNV, hoTen, chucVu, soDienThoai, Email, NgayVaoLam)

        self.load_data()  

    def delete_nhanvien(self):
        selected_row = self.tableNhanVien.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn một nhân viên để xóa!")
            return

        maNV = self.tableNhanVien.item(selected_row, 0).text()

        confirm = QMessageBox.question(
            self, "Xác nhận xóa", f"Bạn có chắc chắn muốn xóa nhân viên có mã {maNV} không?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if confirm == QMessageBox.StandardButton.Yes:
            if self.nhanvien_bus.delete_nhanvien(maNV): 
                self.load_data()
                QMessageBox.information(self, "Thành công", "Đã xóa nhân viên.")
            else:
                QMessageBox.critical(self, "Lỗi", "Không thể xóa nhân viên!")


    def search_nhanvien(self):
        """Tìm kiếm nhân viên theo tên."""
        keyword = self.txtTimKiem.text()
        self.load_data(filter_text=keyword)
    def reset(self):
        self.maNV.clear()
        self.tenNV.clear()
        self.chucVu.clear()
        self.phone.clear()
        self.txtEmail.clear()
        self.txtNgayVaoLam.clear()
    def exit(self):
        self.close()
        self.main_window.show()
if __name__ == "__main__":
    app = QApplication(sys.argv)

    test_window = NhanVien_GUI(None)  
    test_window.show()

    try:
        sys.exit(app.exec())
    except Exception as e:
        print(f"Lỗi khi chạy ứng dụng: {e}")
