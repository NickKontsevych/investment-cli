import argparse
import csv
import termgraph
from prettytable import PrettyTable
from modules.transactions import get_transactions
from modules.portfolio import get_portfolio, get_portfolio_history
from modules.dividends import get_dividends
from modules.analytics import calculate_summary

def show_transactions():
    """Відображає всі транзакції у вигляді таблиці."""
    transactions = get_transactions()
    table = PrettyTable(["ID", "Дата", "Тип", "Тікер", "Кількість", "Ціна", "Сума", "Комісія (%)", "Комісія ($)"])
    for row in transactions:
        table.add_row(row)
    print(table)

def show_portfolio():
    """Відображає поточний портфель у вигляді таблиці."""
    portfolio = get_portfolio()
    table = PrettyTable(["Тікер", "Кількість", "Середня ціна"])
    for row in portfolio:
        table.add_row(row)
    print(table)

def show_dividends():
    """Відображає всі дивіденди у вигляді таблиці."""
    dividends = get_dividends()
    table = PrettyTable(["ID", "Дата", "Тікер", "Сума", "Кількість", "Дивіденди за акцію"])
    for row in dividends:
        table.add_row(row)
    print(table)

def export_to_csv(data, filename, headers):
    """Експортує дані у CSV."""
    if not data:
        print(f"⚠️ Немає даних для експорту ({filename}).")
        return

    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(headers)  # Записуємо заголовки
        writer.writerows(data)  # Записуємо дані
    print(f"✅ Дані експортовано у {filename}")

import os

def show_summary():
    """Відображає загальний підсумок інвестицій."""
    portfolio = get_portfolio()
    transactions = get_transactions()

    total_value = 0  # Загальна вартість портфеля
    total_invested = 0  # Загальна сума інвестицій

    print("\n📊 **АНАЛІЗ ПОРТФЕЛЯ**")

    if portfolio:
        table = PrettyTable(["Тікер", "Кількість", "Середня ціна", "Загальна вартість"])
        for ticker, quantity, avg_price in portfolio:
            total_value += quantity * avg_price
            total_invested += quantity * avg_price  # Тимчасово прирівнюємо до вартості

            table.add_row([ticker, quantity, avg_price, round(quantity * avg_price, 2)])
        print(table)
    else:
        print("❌ Портфель порожній!")

    print(f"\n💰 Загальна вартість портфеля: **{round(total_value, 2)}$**")
    print(f"💵 Загальна сума інвестованих коштів: **{round(total_invested, 2)}$**")

    # ASCII графік для візуалізації портфеля
    if portfolio:
        print("\n📈 **Структура портфеля (графік)**")

        # Створюємо тимчасовий файл для termgraph
        with open("portfolio_data.txt", "w") as f:
            f.write("# Portfolio Distribution\n")
            for row in portfolio:
                f.write(f"{row[0]} {row[1]}\n")  # Тікер, Кількість акцій (без коми)

        # Викликаємо termgraph через командний рядок
        os.system("termgraph portfolio_data.txt")

        # Видаляємо тимчасовий файл після використання
        os.remove("portfolio_data.txt")

def show_portfolio_history():
    """Відображає історію змін портфеля у вигляді таблиці."""
    history = get_portfolio_history()
    
    if not history:
        print("📉 Історія портфеля порожня.")
        return

    table = PrettyTable(["Дата", "Тікер", "Кількість", "Середня ціна", "Загальна вартість"])
    for row in history:
        table.add_row(row)
    print(table)

def main():
    parser = argparse.ArgumentParser(description="Investment CLI - Управління інвестиціями")
    parser.add_argument("command", help="Команда: transactions, portfolio, dividends, export, summary, portfolio_history")
    parser.add_argument("--type", help="Тип експорту (transactions, portfolio, dividends)", required=False)

    args = parser.parse_args()

    if args.command not in ["transactions", "portfolio", "dividends", "export", "summary", "portfolio_history"]:
        print("❌ Невідома команда. Використовуйте одну з:")
        print("   - transactions")
        print("   - portfolio")
        print("   - dividends")
        print("   - export --type transactions|portfolio|dividends")
        print("   - summary")
        print("   - portfolio_history")
        exit(1)

    if args.command == "transactions":
        show_transactions()
    elif args.command == "portfolio":
        show_portfolio()
    elif args.command == "dividends":
        show_dividends()
    elif args.command == "export":
        if args.type == "transactions":
            export_to_csv(get_transactions(), "transactions.csv", 
                          ["ID", "Дата", "Тип", "Тікер", "Кількість", "Ціна", "Сума", "Комісія (%)", "Комісія ($)"])
        elif args.type == "portfolio":
            export_to_csv(get_portfolio(), "portfolio.csv", ["Тікер", "Кількість", "Середня ціна"])
        elif args.type == "dividends":
            export_to_csv(get_dividends(), "dividends.csv", ["ID", "Дата", "Тікер", "Сума", "Кількість", "Дивіденди за акцію"])
        else:
            print("❌ Невідомий тип експорту. Використовуйте: transactions, portfolio, dividends")
    elif args.command == "summary":
        calculate_summary()
    elif args.command == "portfolio_history":
        show_portfolio_history()

if __name__ == "__main__":
    main()