import requests
import pandas as pd

# 1. Адрес API
url = "http://127.0.0.1:8000/orders"

# 2. Параметры запроса
params = {
    "status": "paid",
    "limit": 100,
    "offset": 0
}

# 3. Отправляем GET-запрос
response = requests.get(url, params=params)

# 4. Проверяем, успешно ли выполнен запрос
response.raise_for_status()

# 5. Получаем JSON из ответа
data = response.json()

# 6. Извлекаем список заказов
orders = data["items"]

# 7. Преобразуем список словарей в таблицу
df = pd.DataFrame(orders)

# 8. Выводим результат
print("Всего найдено заказов:", data["total"])
print("\nТаблица заказов:")
print(df.to_string(index=False))

# 13. Преобразуем дату в datetime
df["created_at"] = pd.to_datetime(df["created_at"])

# 9. Исследуем структуру данных
print("\n--- Структура таблицы ---")
df.info()

# 10. Проверяем пропущенные значения
print("\n--- Пропущенные значения ---")
print(df.isna().sum())

# 11. Проверяем дубликаты
print("\n--- Дубликаты ---")
print("Количество дубликатов:", df.duplicated().sum())

# 12. Смотрим статистику числовых столбцов
print("\n--- Статистика ---")
print(df.describe())

# 14. Рассчитываем выручку по заказу
df["revenue"] = (
    df["quantity"] * df["unit_price"] - df["discount"]
)

# 15. Выводим заказы с рассчитанной выручкой
print("\n--- Выручка по заказам ---")
print(
    df[["order_id", "quantity", "unit_price", "discount", "revenue"]]
    .to_string(index=False)
)

# 16. Считаем общую выручку
print("\nОбщая выручка:", df["revenue"].sum())


# Выделяем дату без времени
df["date"] = df["created_at"].dt.date

# Группируем заказы по дате и считаем выручку
daily_revenue = (
    df.groupby("date")
    .agg(
        orders_count=("order_id", "count"),
        revenue=("revenue", "sum")
    )
    .reset_index()
)

print("\n--- Выручка по дням ---")
print(daily_revenue.to_string(index=False))

user_reveue = (
    df.groupby("user_id")
    .agg(
        orders_count=("order_id", "count"),
        revenue=("revenue", "sum")
    )
    .reset_index()
)
print('\n--- Выручка по пользователям ---')
print(user_reveue.to_string(index=False))