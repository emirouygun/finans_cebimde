import sys, os
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.uic import loadUi
from services.auth_service import AuthService
from utils.path_utils import resource_path

class RegisterController(QDialog):
    def __init__(self):
        super().__init__()
        # if getattr(sys, 'frozen', False):
        #     base_path = sys._MEIPASS  # EXE çalışıyorsa geçici klasör
        # else:
        #     base_path = os.path.dirname(os.path.abspath(__file__))

        # ui_path = os.path.join(base_path, "ui", "register.ui")
        # loadUi(ui_path, self)

        ui_path = resource_path("ui/register.ui")
        loadUi(ui_path, self)        
        #loadUi("ui/register.ui", self)

        self.auth_service = AuthService()
        self.btn_register.clicked.connect(self.register)

    def register(self):
        username = self.input_username.text()  # Kullanıcı adı alınıyor
        password = self.input_password.text()  # Şifre alınıyor
        password2 = self.input_password2.text()  # Şifre tekrarı alınıyor

        if not username or not password:
            QMessageBox.warning(self, "HATA", "Kullanıcı adı ve şifre boş olamaz.")
            return
        if password != password2:
            QMessageBox.warning(self, "HATA", "Şifreler eşleşmiyor.")
            return
        
        success = self.auth_service.register_user(username, password)  # Kayıt işlemi

        if success:
            QMessageBox.information(self, "BAŞARILI", "Kayıt başarılı!")
            self.accept()  # Kayıt başarılıysa dialogu kapat
        else:
            QMessageBox.critical(self, "HATA", "Kayıt başarısız. Kullanıcı adı mevcut.")