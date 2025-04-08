class QuanLyKhachHang_w(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('QuanLyKhachHang.ui', self) 
        self.btnAdd.clicked.connect(self.add_row)
        self.btnReset.clicked.connect(self.reset)
        self.btnDel.clicked.connect(self.del_row)
        self.btnEdit.clicked.connect(self.edit_row)
        self.btnExit.clicked.connect(self.open_w)

        self.tableWidget.itemSelectionChanged.connect(self.set_input)
        self.load_data()
    def open_w(self):
        widget.setCurrentIndex(2)
    def load_data(self):
        db = mdb.connect(host="localhost", user="root", password="", database="donghonuoc")
        cursor = db.cursor()
        
        cursor.execute("SELECT maKH, tenKH, diachi, phone, ngayDK FROM khachhang")
        list = cursor.fetchall()

        self.tableWidget.setRowCount(0)
        
        for i, row_data in enumerate(list):
            self.tableWidget.insertRow(i)
            for j, data in enumerate(row_data):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(data)))

        db.close()
    def add_row(self):
        ngay_dang_ky = self.dateDK.date().toString("yyyy-MM-dd")
        row_index = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row_index) 
        self.tableWidget.setItem(row_index, 0, QTableWidgetItem(self.maKH.text()))
        self.tableWidget.setItem(row_index, 1, QTableWidgetItem(self.tenKH.text()))
        self.tableWidget.setItem(row_index, 2, QTableWidgetItem(self.address.text()))
        self.tableWidget.setItem(row_index, 3, QTableWidgetItem(self.phone.text()))
        self.tableWidget.setItem(row_index, 4, QTableWidgetItem(ngay_dang_ky))
        
        db = mdb.connect(host="localhost", user="root", password="", database="donghonuoc")
        query = db.cursor()
        query.execute(f"INSERT INTO khachhang (maKH, tenKH, diachi, phone, ngayDK) VALUES ('{self.maKH.text()}', '{self.tenKH.text()}', '{self.address.text()}', '{self.phone.text()}', '{self.dateDK.text()}')")
        db.commit()
        db.close()
        QMessageBox.information(self,"Thành công","Thêm thành công")

    
    def reset(self):
        self.maKH.clear()
        self.tenKH.clear()
        self.address.clear()
        self.phone.clear()
        self.dateDK.clear()
    
    def del_row(self):
        selected_row = self.tableWidget.currentRow()
        
        if selected_row >= 0:
            maKH_item = self.tableWidget.item(selected_row, 0)  #LẤY CỘT 0
            maKH = maKH_item.text()
            
            reply = QMessageBox.question(
                self, "Xác nhận xóa", 
                f"Bạn có chắc chắn muốn xóa khách hàng có mã '{maKH}' không?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.No:
                return
            
            self.tableWidget.removeRow(selected_row)

            try:
                db = mdb.connect(host="localhost", user="root", password="", database="donghonuoc")
                query = db.cursor()
                
                query.execute(f"DELETE FROM khachhang WHERE maKH = '{maKH}'")
                db.commit() 
                db.close()
                QMessageBox.information(self, "Thành công", "Dữ liệu đã được xóa thành công")  
            except mdb.Error as e:
                QMessageBox.critical(self, "Lỗi", f"Lỗi khi xóa dữ liệu: {e}")
    def set_input(self):
        selected_row = self.tableWidget.currentRow()

        if selected_row < 0:
            return  

        maKH_edit = self.tableWidget.item(selected_row, 0).text()
        tenKH_edit = self.tableWidget.item(selected_row, 1).text()
        diachi_edit = self.tableWidget.item(selected_row, 2).text()
        phone_edit = self.tableWidget.item(selected_row, 3).text()
        ngaydk_edit = self.tableWidget.item(selected_row, 4).text()

        self.maKH.setText(maKH_edit)
        self.tenKH.setText(tenKH_edit)
        self.address.setText(diachi_edit)
        self.phone.setText(phone_edit)
        self.dateDK.setDate(QDate.fromString(ngaydk_edit, "yyyy-MM-dd"))

    def edit_row(self):
        selected_row = self.tableWidget.currentRow()

        if selected_row < 0:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn một hàng để chỉnh sửa!")
            return

        new_maKH = self.maKH.text()
        new_tenKH = self.tenKH.text()
        new_diachi = self.address.text()
        new_phone = self.phone.text()
        new_ngaydk = self.dateDK.date().toString("yyyy-MM-dd")

        self.tableWidget.setItem(selected_row, 0, QTableWidgetItem(new_maKH))
        self.tableWidget.setItem(selected_row, 1, QTableWidgetItem(new_tenKH))
        self.tableWidget.setItem(selected_row, 2, QTableWidgetItem(new_diachi))
        self.tableWidget.setItem(selected_row, 3, QTableWidgetItem(new_phone))
        self.tableWidget.setItem(selected_row, 4, QTableWidgetItem(new_ngaydk))

        try:
            db = mdb.connect(host="localhost", user="root", password="", database="donghonuoc")
            cursor = db.cursor()
            cursor.execute(f"""
                UPDATE khachhang 
                SET tenKH = '{new_tenKH}', diachi = '{new_diachi}', phone = '{new_phone}', ngayDK = '{new_ngaydk}' 
                WHERE maKH = '{new_maKH}'
            """)
            db.commit()
            db.close()

            QMessageBox.information(self, "Thành công", "Dữ liệu đã được cập nhật!")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi cập nhật dữ liệu: {e}")