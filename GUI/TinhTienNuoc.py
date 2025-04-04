from PyQt6.QtWidgets import QMainWindow, QFileDialog
from PyQt6 import uic
from PyQt6.QtGui import QPixmap
from BUS.TinhTienNuocBUS import TinhTienNuocBUS
import cv2
import datetime
import os
import shutil

class TinhTienNuoc(QMainWindow):
    def __init__(self, customer_data):
        super().__init__()
        self.tinhTienNuocBUS = TinhTienNuocBUS()
        uic.loadUi("GUI/UI/tinhTienNuocUI.ui", self)
        
        #? Nút close, submit
        self.btnClose.clicked.connect(self.close)
        
        self.txtMaKH.setText(customer_data["id"])
        self.txtHoTen.setText(customer_data["name"])
        self.txtSoDienThoai.setText(customer_data["phone"])
        self.txtEmail.setText(customer_data["email"])
        self.txtDiaChi.setText(customer_data["address"])
        
        waterMeter = self.tinhTienNuocBUS.getWaterMeterById(customer_data["id"])
        
        self.txtMaDongHoNuoc.setText(str(waterMeter["id"]))
        self.txtSoNuocTruoc.setText(str(waterMeter["meter_number"]))
        
        # Gán sự kiện cho nút "Chụp Ảnh" và "Chọn Ảnh"
        self.btnCapture.clicked.connect(self.capture_image)
        self.btnChoose.clicked.connect(self.open_file_dialog)
    
    def display_image(self, file_path):
        """Hiển thị ảnh lên QLabel"""
        pixmap = QPixmap(file_path)
        self.hinhAnhDaChon.setPixmap(pixmap)
        self.hinhAnhDaChon.setScaledContents(True)  # Đảm bảo ảnh vừa với QLabel
    
    def capture_image(self):
        """Mở camera để chụp ảnh và hiển thị lên QLabel"""
        cap = cv2.VideoCapture(0)  # Mở camera mặc định
        if not cap.isOpened():
            print("Không thể mở camera")
            return

        while True:
            ret, frame = cap.read()
            if not ret or frame is None:
                print("Không thể đọc dữ liệu từ camera")
                break

            cv2.imshow("Chụp Ảnh - Nhấn SPACE để chụp, ESC để thoát", frame)

            key = cv2.waitKey(1)
            if key == 27:  # Nhấn ESC để thoát
                break
            elif key == 32:  # Nhấn SPACE để chụp
                maKH = self.txtMaKH.toPlainText().strip()
                maDHN = self.txtMaDongHoNuoc.toPlainText().strip()

                
                ngayChup = datetime.datetime.now().strftime("%d%m%Y_%H%M%S")
                file_name = f"{maKH}_{maDHN}_{ngayChup}.jpg"
                
                save_dir = "Resource/CaptureIMG"
                os.makedirs(save_dir, exist_ok=True)

                file_path = os.path.join(save_dir, file_name)
                cv2.imwrite(file_path, frame)
                print(f"Ảnh đã được lưu vào : {file_path}")
                self.display_image(file_path)  
                break

        cap.release()
        cv2.destroyAllWindows()
    
    def open_file_dialog(self):
        """Chọn ảnh từ máy tính"""
        file_path, _ = QFileDialog.getOpenFileName(self, "Chọn ảnh", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        
        if file_path:
            self.display_image(file_path)
            print(f"Ảnh đã chọn: {file_path}")

            maKH = self.txtMaKH.toPlainText().strip()
            maDHN = self.txtMaDongHoNuoc.toPlainText().strip()

            
            ngayChup = datetime.datetime.now().strftime("%d%m%Y_%H%M%S")
            file_name = f"{maKH}_{maDHN}_{ngayChup}.jpg"
            
            save_dir = "Resource/ChooseIMG"
            os.makedirs(save_dir, exist_ok=True)

            save_path = os.path.join(save_dir, file_name)
            shutil.copy(file_path, save_path)
            print(f"Ảnh đã được lưu vào: {save_path}")
        else:
            print("Không có ảnh nào được chọn.")
