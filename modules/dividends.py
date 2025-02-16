import sqlite3
import logging
from modules.database import get_db_connection

# Логування помилок
logging.basicConfig(filename="log.txt", level=logging.ERROR, format="%(asctime)s - %(levelень)s - %(message)s")

def add_dividend(date, ticker, amount, shares):
    """
    Додає запис про виплату дивідендів у базу даних.
    :param date: Дата виплати дивідендів (YYYY-MM-DD)
    :param ticker: Символ акції (наприклад, 'AAPL')
    :param amount: Загальна сума виплати ($)
    :param shares: Кількість акцій, на які виплачено дивіденди
    """
    try:
        dividend_per_share = amount / shares if shares > 0 else 0

        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO dividends (date, ticker, amount, shares, dividend_per_share)
            VALUES (?, ?, ?, ?, ?)
            """, (date, ticker, amount, shares, dividend_per_share))

            conn.commit()
            print(f"✅ Дивіденди {ticker}: {amount}$ на {shares} акцій ({dividend_per_share:.2f}$ за акцію).")
    
    except sqlite3.Error as e:
        logging.error(f"❌ Помилка при додаванні дивідендів: {e}")
        print("❌ Помилка при додаванні дивідендів. Деталі в log.txt.")

def get_dividends():
    """
    Отримує всі виплати дивідендів.
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM dividends ORDER BY date DESC")
            dividends = cursor.fetchall()
            return dividends
    
    except sqlite3.Error as e:
        logging.error(f"❌ Помилка при отриманні дивідендів: {e}")
        return []