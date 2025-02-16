import sqlite3
import logging
from modules.database import get_db_connection
from modules.portfolio import update_portfolio, save_portfolio_snapshot

# Логування помилок
logging.basicConfig(filename="log.txt", level=logging.ERROR, format="%(asctime)s - %(levelень)s - %(message)s")

def add_transaction(date, type, ticker=None, quantity=None, price=None, fee_percent=0):
    """
    Додає транзакцію в базу даних та оновлює портфель (BUY/SELL).
    """
    try:
        if type not in ["BUY", "SELL", "DEPOSIT"]:
            print("❌ Невідомий тип угоди. Використовуйте 'BUY', 'SELL' або 'DEPOSIT'.")
            return
        
        if type == "DEPOSIT":
            if price is None or price <= 0:
                print("❌ Некоректна сума для DEPOSIT.")
                return
            ticker = "CASH"
            quantity = None
            fee_amount = 0
            amount = price  # Депозитна сума записується напряму
        
        else:
            if not ticker or not quantity or not price:
                print("❌ Некоректні дані для BUY/SELL.")
                return
            
            fee_amount = (quantity * price) * (fee_percent / 100)  # Розрахунок комісії
            amount = (quantity * price) + fee_amount  # Загальна сума з комісією

        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO transactions (date, type, ticker, quantity, price, amount, fee_percent, fee_amount)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (date, type, ticker, quantity, price, amount, fee_percent, fee_amount))

            conn.commit()
            print(f"✅ Транзакція ({type}) {ticker} на {amount}$ додана.")

            # Оновлення портфеля автоматично при BUY/SELL
            if type in ["BUY", "SELL"]:
                update_portfolio(ticker, quantity, price, type)

            # Викликаємо оновлення історії портфеля після будь-якої транзакції
            save_portfolio_snapshot()
    
    except sqlite3.Error as e:
        logging.error(f"❌ Помилка при додаванні транзакції: {e}")
        print("❌ Помилка при додаванні транзакції. Деталі в log.txt.")

def get_transactions():
    """
    Отримує список усіх транзакцій.
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM transactions ORDER BY date DESC")
            transactions = cursor.fetchall()
            return transactions
    
    except sqlite3.Error as e:
        logging.error(f"❌ Помилка при отриманні транзакцій: {e}")
        return []