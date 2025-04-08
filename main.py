from PyQt6.QtWidgets import QApplication
import sys
from GUI.ClassUI import MyApp
if __name__ == "__main__":  #test ground
    app = QApplication(sys.argv)
    window = MyApp()  # Start with the login window
    window.show()
    sys.exit(app.exec())
    #testing the database function