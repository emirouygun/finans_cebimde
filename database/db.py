import sqlite3
import os
import platform


APP_NAME = "finans_cebimde"

def get_db_path():
    system = platform.system()

    if system == "Windows":
        base_dir = os.environ.get("LOCALAPPDATA")
        if base_dir is None:
            base_dir = os.path.expanduser("~")
        data_dir = os.path.join(base_dir, APP_NAME)

    elif system == "Linux":
        base_dir = os.environ.get("XDG_DATA_HOME",
                                  os.path.join(os.path.expanduser("~"), ".local", "share"))
        data_dir = os.path.join(base_dir, APP_NAME)

    else:
        # macOS vs. fallback
        data_dir = os.path.join(os.path.expanduser("~"), f".{APP_NAME}")

    os.makedirs(data_dir, exist_ok=True)
    return os.path.join(data_dir, "app_database.db")


DB_PATH = get_db_path()

def get_connection():
    """Veritabanı bağlantısı oluşturur ve döner."""
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row # Database'de oluşturulan tabloların satırlarını sözlük olarak döner.
    connection.execute("PRAGMA foreign_keys = ON") # Yabancı anahtar kısıtlamalarını etkinleştirir.
    return connection

def init_db():
    """Veritabanını başlatır ve gerekli tabloları oluşturur."""
    connection = get_connection() # Veritabanı bağlantısını al
    cursor = connection.cursor() # İmleç oluştur

    cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS users (                          
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP)""")
    """
    users tablosu oluşturur. Bu tablo kullanıcı bilgilerini saklar.
    - id: Her kullanıcı için benzersiz bir kimlik numarası.
    - username: Kullanıcının benzersiz kullanıcı adı.
    - password: Kullanıcının şifrelenmiş parolası.
    - created_at: Kullanıcının oluşturulma tarihi ve saati.
    """
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS investments (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   user_id INTEGER NOT NULL,
                   asset TEXT NOT NULL,
                   amount REAL NOT NULL,
                   price REAL NOT NULL,
                   total REAl NOT NULL,
                   created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                   FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE)""")
    """
    investments tablosu oluşturur. Bu tablo kullanıcı yatırımlarını saklar.
    - id: Her yatırım için benzersiz bir kimlik numarası.
    - user_id: Yatırımı yapan kullanıcının kimlik numarası (users tablosuna yabancı anahtar).
    - assest_type: Yatırımın türü (örneğin, hisse senedi, tahvil, kripto para).
    - amount: Yatırım miktarı.
    - created_at: Yatırımın oluşturulma tarihi ve saati.
    """


    connection.commit()
    connection.close()
    
