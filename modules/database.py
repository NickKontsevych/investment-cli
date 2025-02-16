import sqlite3
import logging

# Налаштування логування (запис у файл log.txt)
logging.basicConfig(filename="log.txt", level=logging.ERROR, format="%(asctime)s - %(levelень)s - %(message)s")

# Константа з шляхом до бази (можна змінити на ":memory:" для тестування)
DB_PATH = "investment.db"

# Функція для створення підключення до бази
def get_db_connection():
    """Створює з'єднання з базою даних SQLite."""
    try:
        conn = sqlite3.connect(DB_PATH)
        return conn
    except sqlite3.Error as e:
        logging.error(f"❌ Помилка підключення до бази даних: {e}")
        return None

# Функція для ініціалізації таблиць у базі даних
def initialize_db():
    """Створює таблиці у базі, якщо вони ще не існують."""
    try:
        with sqlite3.connect(DB_PATH) as conn:  # Використання контекстного менеджера (автоматично закриє з'єднання)
            cursor = conn.cursor()

            # Таблиця для транзакцій (купівля/продаж/депозит)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                type TEXT NOT NULL CHECK(type IN ('BUY', 'SELL', 'DEPOSIT')),
                ticker TEXT NOT NULL,
                quantity REAL NOT NULL CHECK(quantity > 0),
                price REAL NOT NULL CHECK(price >= 0),
                amount REAL NOT NULL,
                fee_percent REAL NOT NULL CHECK(fee_percent >= 0),
                fee_amount REAL NOT NULL CHECK(fee_amount >= 0)
            )
            """)

            # Таблиця для поточного портфеля
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS portfolio (
                ticker TEXT PRIMARY KEY,
                quantity REAL NOT NULL CHECK(quantity >= 0),
                avg_price REAL NOT NULL CHECK(avg_price >= 0)
            )
            """)

            # Таблиця для дивідендів
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS dividends (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                ticker TEXT NOT NULL,
                amount REAL NOT NULL CHECK(amount >= 0),
                shares REAL NOT NULL CHECK(shares >= 0),
                dividend_per_share REAL NOT NULL CHECK(dividend_per_share >= 0)
            )
            """)

            # Додавання індексів для пришвидшення пошуку
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_transactions_ticker ON transactions (ticker)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_dividends_ticker ON dividends (ticker)")

            # Таблиця для історії портфеля
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS portfolio_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                ticker TEXT NOT NULL,
                quantity REAL NOT NULL CHECK(quantity >= 0),
                avg_price REAL NOT NULL CHECK(avg_price >= 0),
                total_value REAL NOT NULL CHECK(total_value >= 0)
            )
            """)

            conn.commit()
            print("✅ База даних ініціалізована успішно.")

    except sqlite3.Error as e:
        logging.error(f"❌ Помилка ініціалізації бази даних: {e}")
        print("❌ Помилка при створенні таблиць. Перевірте лог-файл `log.txt`.")

# Виконуємо ініціалізацію бази при першому запуску
if __name__ == "__main__":
    initialize_db()