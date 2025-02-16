import yfinance as yf
from modules.portfolio import get_portfolio
from modules.transactions import get_transactions
from prettytable import PrettyTable
import os

def get_current_price(ticker):
    """Отримує поточну ринкову ціну акції через Yahoo Finance API."""
    try:
        stock = yf.Ticker(ticker)
        current_price = stock.history(period="1d")["Close"].iloc[-1]  # Беремо останню доступну ціну
        return round(float(current_price), 2)
    except Exception as e:
        print(f"⚠️ Помилка отримання ціни для {ticker}: {e}")
        return None

def calculate_summary():
    """Обчислює загальну вартість портфеля, прибуток та ROI."""
    portfolio = get_portfolio()
    transactions = get_transactions()

    total_value = 0  # Поточна вартість портфеля
    total_invested = 0  # Загальна сума інвестованих коштів
    total_profit = 0  # Загальний прибуток
    roi = 0  # ROI у %

    if portfolio:
        table = PrettyTable(["Тікер", "Кількість", "Середня ціна", "Поточна ціна", "Загальна вартість", "Прибуток/Збиток"])
        for ticker, quantity, avg_price in portfolio:
            current_price = get_current_price(ticker)  # Отримуємо актуальну ціну

            if current_price is None:
                current_price = avg_price  # Якщо не вдалося отримати ціну, використовуємо середню ціну покупки

            current_value = quantity * current_price  # Поточна вартість
            total_value += current_value
            total_invested += quantity * avg_price  # Витрати на покупку

            # Новий розрахунок прибутку/збитку
            profit = (current_price - avg_price) * quantity
            total_profit += profit

            table.add_row([ticker, quantity, avg_price, round(current_price, 2), round(current_value, 2), round(profit, 2)])

        print("\n📊 **АНАЛІЗ ПОРТФЕЛЯ**")
        print(table)
    else:
        print("❌ Портфель порожній!")

    # Обчислення ROI
    if total_invested > 0:
        roi = (total_profit / total_invested) * 100

    print(f"\n💰 Загальна вартість портфеля: **{round(total_value, 2)}$**")
    print(f"💵 Загальна сума інвестованих коштів: **{round(total_invested, 2)}$**")
    print(f"📈 **Загальний прибуток/збиток:** **{round(total_profit, 2)}$**")
    print(f"📊 **ROI:** **{round(roi, 2)}%**")

    # ASCII графік для візуалізації портфеля
    if portfolio:
        print("\n📈 **Структура портфеля (графік)**")

        # Створюємо тимчасовий файл для termgraph
        with open("portfolio_data.txt", "w") as f:
            f.write("# Portfolio Distribution\n")
            for row in portfolio:
                f.write(f"{row[0]} {row[1]}\n")  # Тікер, Кількість акцій

        # Викликаємо termgraph через командний рядок
        os.system("termgraph portfolio_data.txt")

        # Видаляємо тимчасовий файл після використання
        os.remove("portfolio_data.txt")