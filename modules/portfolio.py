import sqlite3
import logging
from modules.database import get_db_connection

# Логування помилок
logging.basicConfig(filename="log.txt", level=logging.ERROR, format="%(asctime)s - %(levelень)s - %(message)s")

def update_portfolio(ticker, quantity, price, transaction_type):
    """
    Оновлює портфель при купівлі або продажу акцій.
    :param ticker: Символ акції (наприклад, 'AAPL')
    :param quantity: Кількість акцій
    :param price: Ціна за одиницю
    :param transaction_type: Тип угоди ('BUY' або 'SELL')
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()

            # Отримуємо поточну кількість акцій і середню ціну
            cursor.execute("SELECT quantity, avg_price FROM portfolio WHERE ticker = ?", (ticker,))
            row = cursor.fetchone()

            if transaction_type == "BUY":
                if row:  
                    old_quantity, old_avg_price = row
                    new_quantity = old_quantity + quantity
                    new_avg_price = ((old_quantity * old_avg_price) + (quantity * price)) / new_quantity
                else:
                    new_quantity = quantity
                    new_avg_price = price

                cursor.execute("""
                INSERT INTO portfolio (ticker, quantity, avg_price) 
                VALUES (?, ?, ?)
                ON CONFLICT(ticker) 
                DO UPDATE SET quantity = excluded.quantity, avg_price = excluded.avg_price
                """, (ticker, new_quantity, new_avg_price))

            elif transaction_type == "SELL":
                if row and row[0] >= quantity:
                    new_quantity = row[0] - quantity
                    if new_quantity == 0:
                        cursor.execute("DELETE FROM portfolio WHERE ticker = ?", (ticker,))
                    else:
                        cursor.execute("UPDATE portfolio SET quantity = ? WHERE ticker = ?", (new_quantity, ticker))
                else:
                    print("❌ Помилка: Немає достатньо акцій для продажу!")
                    return

            conn.commit()
            print(f"✅ Портфель оновлено: {transaction_type} {quantity} {ticker} по {price}$")
    
    except sqlite3.Error as e:
        logging.error(f"❌ Помилка при оновленні портфеля: {e}")
        print("❌ Помилка при оновленні портфеля. Деталі в log.txt.")

def get_portfolio():
    """
    Отримує всі активи з портфеля.
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM portfolio")
            portfolio = cursor.fetchall()
            return portfolio
    
    except sqlite3.Error as e:
        logging.error(f"❌ Помилка при отриманні портфеля: {e}")
        return []

def save_portfolio_snapshot():
    """Зберігає поточний стан портфеля в історію."""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            portfolio = get_portfolio()

            for ticker, quantity, avg_price in portfolio:
                total_value = quantity * avg_price
                cursor.execute("""
                INSERT INTO portfolio_history (date, ticker, quantity, avg_price, total_value)
                VALUES (datetime('now'), ?, ?, ?, ?)
                """, (ticker, quantity, avg_price, total_value))

            conn.commit()
            print("📌 Історія портфеля оновлена.")
    
    except sqlite3.Error as e:
        logging.error(f"❌ Помилка при збереженні історії портфеля: {e}")
        print("❌ Помилка при збереженні історії портфеля.")