import os
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# 1. Определяем корень проекта
PROJECT_DIR = Path(__file__).resolve().parent.parent
# 2. Загружаем настройки подключения
load_dotenv(PROJECT_DIR / ".env")

# 3. Формируем строку подключения
connection_url = (
    f"postgresql+psycopg://"
    f"{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}"
    f"/{os.getenv('DB_NAME')}"
)

# 4. Создаём Engine
engine = create_engine(connection_url)

# 5. Находим CSV
csv_path = PROJECT_DIR / "data" / "processed" / "sales_mart.csv"

# 6. Загружаем CSV в DataFrame
sales_mart = pd.read_csv(csv_path)
sales_mart["created_at"] = pd.to_datetime(sales_mart["created_at"])

if sales_mart.empty:
    print("Нет новых данных. Загрузка не требуется.")
    engine.dispose()
    raise SystemExit(0)

new_last_order_id = int(sales_mart["order_id"].max())

print("Новый Watermark:", new_last_order_id)

print("Получено строк:", len(sales_mart))

# Получаем последнюю контрольную точку
with engine.connect() as connection:
    result = connection.execute(
        text("""
            SELECT last_order_id
            FROM etl_watermarks
            WHERE pipeline_name = :pipeline_name
        """),
        {"pipeline_name": "sales_mart"}
    )

    last_order_id = result.scalar_one()

print("Последний обработанный заказ:", last_order_id)

if new_last_order_id <= last_order_id:
    print("Новых заказов нет. Загрузка не требуется.")
    engine.dispose()
    raise SystemExit(0)

# 7. Загружаем DataFrame в PostgreSQL
with engine.begin() as connection:
    connection.execute(
        text("TRUNCATE TABLE staging_sales_mart")
    )

    sales_mart.to_sql(
        name="staging_sales_mart",
        con=connection,
        if_exists="append",
        index=False
    )

    print("Данные успешно добавлены в таблицу staging_sales_mart!")

# 8. Переносим данные из staging в основную таблицу
with engine.begin() as connection:
    # Проверяем staging на дубликаты
    duplicates = connection.execute(
        text("""
            SELECT COUNT(*)
            FROM (
                SELECT order_id
                FROM staging_sales_mart
                GROUP BY order_id
                HAVING COUNT(*) > 1
            ) AS duplicate_orders
        """)
    ).scalar()

    if duplicates > 0:
        raise ValueError("В staging обнаружены дубликаты order_id!")

    # Проверяем обязательные поля
    null_rows = connection.execute(
        text("""
            SELECT COUNT(*)
            FROM staging_sales_mart
            WHERE order_id IS NULL
                OR created_at IS NULL
                OR user_id IS NULL
                OR quantity IS NULL
                OR unit_price IS NULL
                OR revenue IS NULL
                OR product_id IS NULL
        """)
    ).scalar()

    if null_rows > 0:
        raise ValueError("В staging обнаружены NULL в обязательных полях!")

    # Переносим проверенные данные
    connection.execute(text("""
        INSERT INTO sales_mart (
            order_id,
            created_at,
            user_id,
            product_id,
            city,
            channel,
            product_name,
            category,
            quantity,
            unit_price,
            discount,
            revenue
        )
        SELECT
            order_id,
            created_at,
            user_id,
            product_id,
            city,
            channel,
            product_name,
            category,
            quantity,
            unit_price,
            discount,
            revenue
        FROM staging_sales_mart
        
        ON CONFLICT (order_id)
        DO UPDATE SET
            created_at = EXCLUDED.created_at,
            user_id = EXCLUDED.user_id,
            product_id = EXCLUDED.product_id,
            city = EXCLUDED.city,
            channel = EXCLUDED.channel,
            product_name = EXCLUDED.product_name,
            category = EXCLUDED.category,
            quantity = EXCLUDED.quantity,
            unit_price = EXCLUDED.unit_price,
            discount = EXCLUDED.discount,
            revenue = EXCLUDED.revenue
    """))

    print("Основная витрина успешно обновлена!")

    connection.execute(
        text("""
            UPDATE etl_watermarks
            SET last_order_id = :new_last_order_id,
                updated_at = CURRENT_TIMESTAMP
            WHERE pipeline_name = :pipeline_name
        """),
        {
            "new_last_order_id": new_last_order_id,
            "pipeline_name": "sales_mart"
        }
    )

    print("Watermark успешно обновлён:", new_last_order_id)