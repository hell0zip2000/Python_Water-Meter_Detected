import tkinter as tk
from tkinter import ttk
from BUS.KhachHangBUS import KhachHangBUS

class KhachHangGUI:
    def __init__(self):
        self.khachhang_bus = KhachHangBUS()

    def show_all(self):
        """In danh sách khách hàng ra màn hình"""
        users = self.khachhang_bus.get_all()
        print("\nDanh sách khách hàng:")
        for user in users:
            print(f"ID: {user.user_id}, Name: {user.name}, Email: {user.email}")

    def close(self):
        self.khachhang_bus.close()