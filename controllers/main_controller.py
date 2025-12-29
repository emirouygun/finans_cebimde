import sys, os
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QTableWidgetItem, QMessageBox
from PyQt5.QtCore import QTimer
from PyQt5.uic import loadUi
from services.exchange_service import ExchangeService
from ui.mpl_canvas import MplCanvas
from controllers.login_controller import LoginController
from controllers.register_controller import RegisterController
from controllers.change_password_controller import ChangePasswordController
from services.investment_service import InvestmentService
from services.auth_service import AuthService
from utils.path_utils import resource_path

class MainController(QMainWindow):
    def __init__(self):
        super().__init__()
        # if getattr(sys, 'frozen', False):    # Eğer exe dosyası çalışıyorsa, çalışmıyorsa else bloğu
        #     base_path = sys._MEIPASS  # EXE çalışıyorsa geçici klasör
        # else:
        #     base_path = os.path.dirname(os.path.abspath(__file__))
        # ui_path = os.path.join(base_path, "ui", "main.ui")
        # loadUi(ui_path, self)

        ui_path = resource_path("ui/main.ui")
        loadUi(ui_path, self)
        #loadUi("ui/main.ui", self)

        self.current_user = None # Mevcut kullanıcı bilgisi
        
        self.chech_auth_tabs() # Giriş durumuna göre sekmeleri kontrol et
        
        self.btn_login.clicked.connect(self.open_login)
        self.btn_logout.clicked.connect(self.logout)
        self.btn_change_account.clicked.connect(self.change_account)
        self.btn_register.clicked.connect(self.open_register)
        self.btn_change_password.clicked.connect(self.open_change_password)
        self.btn_add_investment.clicked.connect(self.add_investment)        
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_exchange_rates)
        self.timer.start(2000)

        self.gold_prices = []
        self.time_index = []

        self.canvas = MplCanvas(self)
        layout = self.graphWidget.layout()
        if layout is None:
            layout = QVBoxLayout(self.graphWidget)
            self.graphWidget.setLayout(layout)
        layout.addWidget(self.canvas)
        self.btn_convert.clicked.connect(self.convert_currency)

        self.update_profile_ui() 

        self.update_exchange_rates()
        if self.current_user:
            self.load_investments()

    def update_exchange_rates(self):
        try: 
            rates = ExchangeService.get_rates()   # Veriler çekiliyor
            # print(rates)
            self.label_usd.setText(rates.get("DOLAR", "-"))
            self.label_eur.setText(rates.get("EURO", "-"))
            self.label_gold.setText(rates.get("GRAM ALTIN", "-"))
            self.label_sterlin.setText(rates.get("STERLİN", "-"))
            self.label_bist.setText(rates.get("BIST 100", "-"))
            self.label_silver.setText(rates.get("GRAM GÜMÜŞ", "-"))
            self.label_bit.setText(rates.get("BITCOIN", "-"))
            self.label_brent.setText(rates.get("BRENT", "-"))

        except Exception as e:
            print("Veri çekme hatası:", e)

        gold_text = rates.get("GRAM ALTIN")
        if gold_text:
            gold_value = gold_text.replace(".", "").replace(",", ".")
            gold_value = float(gold_value)
            self.update_gold_graph(gold_value) 

    def update_gold_graph(self, gold_price):
        self.gold_prices.append(gold_price)
        self.time_index.append(len(self.gold_prices))
        
        self.gold_prices = self.gold_prices[-20:]
        self.time_index = self.time_index[-20:]

        self.canvas.ax.clear()
        self.canvas.ax.plot(self.time_index, self.gold_prices, marker='o')
        self.canvas.ax.set_title("Gram Altın (Canlı)")
        self.canvas.ax.set_xlabel("Zaman")
        self.canvas.ax.set_ylabel("Fiyat (TL)")

        self.canvas.draw()

    def convert_currency(self):
        try:
            amount_text = self.input_amount.text()
            if not amount_text:
                self.label_result.setText("Miktar Giriniz")
                return
            
            amount = float(amount_text)
            from_currency = self.combo_from.currentText() 

            rates = ExchangeService.get_rates()
            rate_text = rates.get(from_currency)

            if not rate_text:
                self.label_result.setText("Kur Bulunamadı")
                return
            
            rate_value = float(rate_text.replace(".", "").replace(",", "."))
            result = amount * rate_value
            self.label_result.setText(f"{result:.2f} TL")

        except Exception as e:
            self.label_result.setText("Hatalı Giriş")
            print("Dönüştürme hatası:", e)


    def update_profile_ui(self):
        if self.current_user:
            username = self.current_user["username"]
            self.lbl_username.setText(f"Hoş Geldin: {username}")
            
            self.widget_guest.hide()
            self.widget_user.show()
        else:
            self.widget_user.hide()
            self.widget_guest.show()

    def chech_auth_tabs(self):
        if self.current_user:
            self.tabWidget.setTabEnabled(3, True)
        else:
            self.tabWidget.setTabEnabled(3, False)
    
    def open_login(self):
        login = LoginController()
        if login.exec_() == login.Accepted:
            self.current_user = AuthService.current_user
            self.chech_auth_tabs()
            self.update_profile_ui()
            self.load_investments()

    def logout(self):
        AuthService.current_user = None
        self.current_user = None
        self.chech_auth_tabs()
        self.table_investments.setRowCount(0)  # Yatırımları temizle
        self.update_profile_ui()

    def change_account(self):
        self.logout()
        self.open_login()

    def open_register(self):
        register = RegisterController()
        register.exec_()

    def open_change_password(self):
        if not self.current_user: # Kullanıcı giriş yapmamışsa
            return 
        
        change_password = ChangePasswordController(self.current_user) 
        change_password.exec_()

    def add_investment(self):
        asset = self.combo_asset.currentText()
        amount_text = self.input_amount_invest.text()

        if not amount_text:
            QMessageBox.warning(self, "Hata", "Lütfen miktar giriniz.")
            return 
        try:
            amount = float(amount_text)
        except ValueError:
            QMessageBox.warning(self, "Hata", "Geçersiz miktar.")
            return
        
        rates = ExchangeService.get_rates() # Güncel kur bilgisi
        price_text = rates.get(asset)

        if not price_text:
            QMessageBox.warning(self, "Hata", "Seçilen varlık için fiyat bulunamadı.")
            return
        
        price = float(price_text.replace(".","").replace(",", "."))

        InvestmentService.add_investment(asset, amount, price) # DB'e ekle

        self.load_investments() # Yatırımları yenile
        self.input_amount_invest.clear()
    
    def load_investments(self):

        investments = InvestmentService.get_user_investment()
        self.table_investments.setRowCount(0)  # Tabloyu temizle
        
        for row_index, inv in enumerate(investments):
            self.table_investments.insertRow(row_index)
            
            total = inv["amount"] * inv["price"]

            self.table_investments.setItem(row_index, 0, QTableWidgetItem(inv["asset"]))
            self.table_investments.setItem(row_index, 1, QTableWidgetItem(str(inv["amount"])))
            self.table_investments.setItem(row_index, 2, QTableWidgetItem(f"{inv['price']:.2f}"))
            self.table_investments.setItem(row_index, 3, QTableWidgetItem(f"{total:.2f}"))
            self.table_investments.setItem(row_index, 4, QTableWidgetItem(inv["created_at"]))