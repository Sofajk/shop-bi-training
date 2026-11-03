import os
from pathlib import Path
import pandas as pd
import requests
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

BASE_URL = "http://127.0.0.1:8000"
# Определяем корень проекта
PROJECT_DIR = Path(__file__).resolve().parent.parent
# Загружаем настройки
load_dotenv(PROJECT_DIR / ".env")
# Подключаемся к PostgreSQL
connection_url = (
    f"postgresql+psycopg://"
    f"{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}"
    f"/{os.getenv('DB_NAME')}"
)

engine = create_engine(connection_url)

# Получаем последний обработанный order_id
with engine.connect() as connection:
    last_order_id = connection.execute(
        text("""
            SELECT last_order_id
            FROM etl_watermarks
            WHERE pipeline_name = :pipeline_name
        """),
        {"pipeline_name": "sales_mart"}
    ).scalar_one()

    print("Последний обработанный заказ:", last_order_id)

all_orders = []

limit = 100
offset = 0

while True:
    orders_response = requests.get(
        BASE_URL + "/orders",
        params={
            "order_id_from": last_order_id,
            'status': 'paid',
            "limit": limit,
            "offset": offset
        }
    )

    orders_response.raise_for_status()

    page_orders = orders_response.json()["items"]

    all_orders.extend(page_orders)

    print(f"Получено заказов: {len(page_orders)}, offset: {offset}")

    if len(page_orders) < limit:
        break

    offset += limit

if not all_orders:
    print("Новых заказов нет. Загрузка не требуется.")
    raise SystemExit(0)

orders = pd.DataFrame(all_orders)

users_response = requests.get(
    BASE_URL + "/users",
)

users_response.raise_for_status()
users = pd.DataFrame(users_response.json()['items'])

products_response = requests.get(
    BASE_URL + "/products",
)

products_response.raise_for_status()
products = pd.DataFrame(products_response.json()['items'])

print('Заказы:')
print(orders.head())
print('\nПользователи:')
print(users.head())
print('\nТовары:')
print(products.head())


orders_users = orders.merge(
    users,
    on="user_id",
    how="left"
)

print("\n--- Заказы с информацией о пользователях ---")
print(orders_users.head().to_string(index=False))

products = products.rename(
    columns={"unit_price": "catalog_price"}
)

orders_users_products = orders_users.merge(
    products,
    on="product_id",
    how="left"
)

print("\n--- Заказы с информацией о пользователях и товарах ---")
print(orders_users_products.head().to_string(index=False))

# Рассчитываем выручку
orders_users_products["revenue"] = (
    orders_users_products["quantity"]
    * orders_users_products["unit_price"]
    - orders_users_products["discount"]
)

# Формируем аналитическую витрину
sales_mart = orders_users_products[
    [
        "order_id",
        "created_at",
        "user_id",
        'product_id',
        "city",
        "channel",
        "product_name",
        "category",
        "quantity",
        "unit_price",
        "discount",
        "revenue"
    ]
].copy()

# Путь к папке processed
OUTPUT_DIR = PROJECT_DIR / "data" / "processed"
# Создаём папку, если её нет
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
# Сохраняем витрину
output_file = OUTPUT_DIR / "sales_mart.csv"

sales_mart.to_csv(
    output_file,
    index=False,
    encoding="utf-8-sig"
)

print(f"\nВитрина сохранена: {output_file}")