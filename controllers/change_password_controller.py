import sys, os
from PyQt5.QtWidgets import QMessageBox, QDialog
from PyQt5.uic import loadUi
from services.auth_service import AuthService
from utils.path_utils import resource_path

class ChangePasswordController(QDialog):
    def __init__(self,user):
        super().__init__()
        # if getattr(sys, 'frozen', False): # frozen kontrolü (frozen: EXE yapısı için)
        #     base_path = sys._MEIPASS  # EXE çalışıyorsa geçici klasör
        # else:
        #     base_path = os.path.dirname(os.path.abspath(__file__))

        # ui_path = os.path.join(base_path, "ui", "change_password.ui")
        # loadUi(ui_path, self)
        ui_path = resource_path("ui/change_password.ui")
        loadUi(ui_path, self)
        #loadUi("ui/change_password.ui", self)

        self.user = user # Mevcut kullanıcı bilgisi
        self.auth_service = AuthService()
        self.btn_change_password.clicked.connect(self.change_password)

    def change_password(self):
        old_password = self.input_old_password.text()  # Eski şifre alınıyor
        new_password = self.input_new_password.text()  # Yeni şifre alınıyor
        new_password2 = self.input_new_password_repeat.text() # Yeni şifre tekrarı alınıyor

        if not old_password or not new_password:
            QMessageBox.warning(self, "HATA", "Alanlar boş olamaz.")
            return
        if new_password != new_password2:
            QMessageBox.warning(self, "HATA", "Yeni şifreler eşleşmiyor.")
            return

        success = self.auth_service.change_password(self.user['id'], old_password, new_password)  # Şifre değiştirme işlemi 

        if success:
            QMessageBox.information(self, "BAŞARILI", "Şifre başarıyla değiştirildi!")
            self.accept()  # Şifre değiştirildiyse dialogu kapat
        else:
            QMessageBox.critical(self, "HATA", "Eski şifre yanlış.") 