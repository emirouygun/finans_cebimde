import sys
from PyQt5.QtWidgets import QApplication
from controllers.main_controller import MainController
from database.db import init_db

def main():
    init_db()  # Veritabanını başlat
    app = QApplication(sys.argv) # PyQt5 uygulamasını başlat
    window = MainController() # Ana denetleyiciyi oluştur
    window.show() # Ana pencereyi göster

    sys.exit(app.exec_()) # Uygulama döngüsünü başlat

if __name__ == "__main__":
    main()