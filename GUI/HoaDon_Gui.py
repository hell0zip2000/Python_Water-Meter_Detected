from PyQt6.QtWidgets import QMainWindow, QMessageBox
from PyQt6.uic import loadUi
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

class QuanLyHoaDon_w(QMainWindow):
    def __init__(self, main_GUI):
        super().__init__()
        uic.loadUi('GUI/UI/QuanLyHoaDon.ui', self) 
        self.mainWindow = main_GUI
        
        self.btnExit.clicked.connect(self.exit_f)
    def exit_f(self):
        self.close()
        self.mainWindow.show()