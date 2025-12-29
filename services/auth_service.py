from database.db import get_connection
# hash kodu yazılarak şifre güvenliği sağlanabilir.

class AuthService:
    current_user = None  # aktif kullanıcı

    @classmethod  # her yerde aynı kullanıcıyı tutmak için sınıf metodu
    def register_user(cls, username: str, password: str) -> bool:
        connection = get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            connection.commit()
            return True
        
        except Exception:
            return False
        
        finally:
            connection.close()

    @classmethod
    def login_user(cls, username: str, password: str): # kullanıcı girişi yapma
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT id, username FROM users WHERE username = ? AND password = ?", (username, password))

        user = cursor.fetchone()
        connection.close()

        if user:
            cls.current_user = {
                "id": user[0],
                "username": user[1]
            }
        return user
    
    @classmethod
    def logout(cls):  # kullanıcıyı çıkış yapma
        cls.current_user = None

    @classmethod
    def is_authenticated(cls):  # kullanıcı giriş yapmış mı kontrol etme
        return cls.current_user is not None
    
    def change_password(self, user_id: int, old_password: str, new_password: str) -> bool:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT id FROM users WHERE id = ? AND password = ?", (user_id, old_password))
        user = cursor.fetchone()

        if not user:
            connection.close()
            return False  # eski şifre yanlış
        
        cursor.execute("UPDATE users SET password = ? WHERE id = ?", (new_password, user_id))

        connection.commit()
        connection.close()
        return True  # şifre değiştirildi
    