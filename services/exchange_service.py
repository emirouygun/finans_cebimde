import requests
from bs4 import BeautifulSoup

class ExchangeService:
    URL = "https://www.doviz.com"

    @staticmethod
    def get_rates():
        response = requests.get(ExchangeService.URL, timeout=5)  # siteye istek atılıyor
        soup = BeautifulSoup(response.text, "html.parser")       # HTML parse ediliyor

        data = {}  # Verilerin saklanacağı sözlük
        items = soup.select("div.market-data div.item") # İlgili HTML elemanları seçiliyor

        for item in items:
            name = item.select_one(".name")  # Döviz adı
            value = item.select_one(".value") # Döviz değeri

            if name and value:
                data[name.text.strip()] = value.text.strip() # Sözlüğe ekleme

        return data
    