# FINANS CEBIMDE MASAUSTU UYGULAMASI

**Finans Cebimde**, kullanıcıların döviz, altın, gümüş gibi finansal varlıkların güncel değerlerini takip edebileceği, basit bir masaüstü uygulamasıdır. Ayrıca kullanıcılar kendi yatırımlarını ekleyip takip edebilir, profil yönetimi yapabilir.  
Bu proje PyQt5 kullanılarak geliştirilmiş bir GUI uygulamasıdır ve SQLite3 tabanlı bir veritabanı ile çalışmaktadır.

## Proje Yapısı

>- finans_cebimde/  
>   - controllers/  
>        - main_controller.py
>        - login_controller.py
>        - change_password_controller.py
>        - register_controller.py
>   -   services/
>        - auth_service.py
>        - exchange_service.py
>        - investment_service.py   
>    - database/
>        - db.py
>   -   ui/
>        - main.ui
>        - login.ui
>        - change_password.ui
>        - register.ui   
>        - mpl_canvas.py
>    - main.py


# Controllers
Controllerlar, UI ile servisler arasındaki ara katmandır. Tüm kullanıcı etkileşimlerini işler:

- MainController  
    Ana sekmeler: Döviz/Altın, Dönüştürme, Grafik, Yatırımlar, Profil   
    Timer ile döviz ve altın verilerini 2 saniyede bir günceller  
    Altın verilerini matplotlib grafiğinde canlı gösterir  
    Yatırımları tabloya yükler ve ekleme işlemlerini yönetir  
    Kullanıcı login/logout işlemlerini kontrol eder 

- LoginController  
    Kullanıcı giriş ve kayıt ekranını yönetir  
    AuthService ile iletişime geçerek doğrulama yapar  

- RegisterController  

- ChangePasswordController  

# Services
Servisler, iş mantığını ve veritabanı işlemlerini kapsar:

- AuthService  
    Kullanıcı kayıt, login ve logout işlemleri   
    current_user değişkeni ile mevcut kullanıcı bilgisini saklar

- ExchangeService  
    Döviz ve altın verilerini webden çeker     
    Kullanıcı arayüzüne JSON/dict olarak verileri iletir

- InvestmentService  
    Kullanıcı yatırımlarını ekler, çeker ve günceller       
    Veriler SQLite3 veritabanında investments tablosunda saklanır

----

# Uygulama Özellikleri

1. Döviz ve Altın Takibi
    - USD, EUR, Gram Altın, Gram Gümüş, Sterlin, Bitcoin, BIST100 ve Brent fiyatları  
    - 2 saniyede bir güncel veriler çekilir
2. Altın ve Döviz Dönüştürme
    - Kullanıcı girdiği miktarı seçilen para birimine dönüştürür  
    - Sonuç TL olarak gözükür
3. Canlı Altın Grafiği
    - Son 20 fiyat verisini matplotlib ile çizer
    - Grafikte zaman ve fiyat eksenleri bulunur
4. Yatırımlarım Sekmesi
    - Sadece login olmuş kullanıcı erişebilir
    - Yeni yatırım ekleme, tablo güncelleme ve toplam değer hesaplama
5. Profilim Sekmesi
    - Kullanıcı adı görüntülenir
    - Şifre değiştirme ve hesap yönetimi yapılabilir

--- 
# INSTALLATION
```
pip install pyqt5
pip install matplotlib
pip install requests
pip install beautifulsoup4
pip install pyinstaller
```
Bu projede **requirements.txt** kullanılmamıştır.
Gerekli kütüphaneler yukarıda manuel olarak listelenmiştir.

Uygulamayı terminalden manuel çalıştırmak için:

```
python3 main.py
``` 
---
## Executable Dosya Üretmek

Windows için .exe dosya üretmek için terminalde :
```
pyinstaller --onefile --windowed --name finans_cebimde --add-data "ui;ui" main.py
```

Linux için executable dosya üretmek için:
```
pyinstaller --onefile --windowed --name finans_cebimde --add-data "ui:ui" main.py
``` 