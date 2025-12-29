import sys, os
from PyQt5.QtWidgets import QMessageBox, QDialog
from PyQt5.uic import loadUi
from services.auth_service import AuthService
from utils.path_utils import resource_path

class LoginController(QDialog):
    def __init__(self):
        super().__init__()
        # if getattr(sys, 'frozen', False):
        #     base_path = sys._MEIPASS  # EXE çalışıyorsa geçici klasör
        # else:
        #     base_path = os.path.dirname(os.path.abspath(__file__))

        # ui_path = os.path.join(base_path, "ui", "login.ui")
        # loadUi(ui_path, self)
        ui_path = resource_path("ui/login.ui")
        loadUi(ui_path, self)
        #loadUi("ui/login.ui", self)

        self.auth_service = AuthService()
        self.user = None
        self.btn_login.clicked.connect(self.login)

    def login(self):
        username = self.input_username.text() # Kullanıcı adı alınıyor
        password = self.input_password.text() # Şifre alınıyor

        if not username or not password:        # Boş alan kontrolü
            QMessageBox.warning(self, "HATA", "Kullanıcı adı ve şifre boş olamaz.")
            return
        
        user = self.auth_service.login_user(username, password)  # Giriş işlemi

        if user:
            self.user = user
            self.accept()  # Giriş başarılıysa dialogu kapat
        else:
            QMessageBox.critical(self, "HATA", "Kullanıcı adı veya şifre yanlış.")
