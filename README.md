📈 Investment CLI

CLI-додаток для управління інвестиційним портфелем.Дозволяє відстежувати купівлі/продажі акцій, депозити, дивіденди, а також отримувати поточні ціни активів через Yahoo Finance.

🚀 Встановлення та запуск

1️⃣ Встановлення залежностей

pip install -r requirements.txt

2️⃣ Запуск CLI

python main.py --help

Виведе список доступних команд.

📌 Команди CLI

🔹 1. Додавання транзакції (BUY, SELL, DEPOSIT)

📌 Формат команди:

from modules.transactions import add_transaction
add_transaction("YYYY-MM-DD", "TYPE", "TICKER", QUANTITY, PRICE, FEE_PERCENT)

📌 Параметри:

YYYY-MM-DD – дата транзакції

TYPE – тип угоди: "BUY", "SELL", "DEPOSIT"

TICKER – тикер активу (наприклад, AAPL, TSLA)

QUANTITY – кількість куплених або проданих акцій

PRICE – ціна за одиницю активу (або сума для DEPOSIT)

FEE_PERCENT – комісія брокера у відсотках

📌 Приклад:

add_transaction("2025-02-20", "BUY", "AAPL", 10, 150.0, 0.2)

🔹 2. Перегляд транзакцій

python main.py transactions

Виведе таблицю всіх транзакцій у базі даних.

🔹 3. Перегляд портфеля

python main.py portfolio

Відобразить поточний список активів у портфелі.

🔹 4. Додавання дивідендів

📌 Формат команди:

from modules.dividends import add_dividend
add_dividend("YYYY-MM-DD", "TICKER", AMOUNT, SHARES)

📌 Параметри:

YYYY-MM-DD – дата виплати дивідендів

TICKER – тикер компанії

AMOUNT – загальна виплата

SHARES – кількість акцій, на які виплачено дивіденди

📌 Приклад:

add_dividend("2025-02-21", "AMZN", 12.0, 5)

🔹 5. Перегляд дивідендів

python main.py dividends

Виведе таблицю виплат дивідендів.

🔹 6. Отримання аналітики портфеля

python main.py summary

Відобразить актуальну вартість портфеля, ROI та поточні ціни активів через Yahoo Finance.

📌 Оновлення цін через Yahoo Finance

Коли виконується команда summary, поточні ціни акцій автоматично завантажуються через Yahoo Finance.

📌 Формат:

from modules.analytics import get_current_price
price = get_current_price("AAPL")

📌 Приклад:

from modules.analytics import calculate_summary
calculate_summary()

🔧 Nick

Investment CLI розроблено для автоматизованого управління портфелем та моніторингу інвестицій.

