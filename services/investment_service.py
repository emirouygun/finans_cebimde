from database.db import get_connection
from services.auth_service import AuthService

class InvestmentService:

    @staticmethod
    def add_investment(asset, amount, price): # yatırım ekleme
        user = AuthService.current_user
        if not user:
            return False
        
        conn = get_connection()
        cur = conn.cursor()

        total = amount * price
        cur.execute("""INSERT INTO investments (user_id, asset, amount,price, total) VALUES (?, ?, ?, ?, ?)""", (user["id"], asset, amount, price, total))
        conn.commit()
        conn.close()
        return True
    
    @staticmethod
    def get_investments():   # yatırım geçmişini getirme
        user = AuthService.current_user  # aktif kullanıcı
        if not user:
            return []
        
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""SELECT asset, amount, price, created_at FROM investments WHERE user_id = ? ORDER BY created_at DESC""", (user["id"],))

        rows = cur.fetchall()
        conn.close()
        return rows
    
    @staticmethod
    def get_user_investment():  # kullanıcının yatırımlarını getirme
        user = AuthService.current_user
        if not user:
            return []
        
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""SELECT asset, amount, price, total, created_at FROM investments WHERE user_id = ? ORDER BY created_at DESC""", (user["id"],))

        rows = cur.fetchall()
        conn.close()
        return rows