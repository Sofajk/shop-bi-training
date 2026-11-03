
import os
from pathlib import Path

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


def build_star_schema():
    with engine.begin() as connection:

        # 5. Проверяем наличие данных
        sales_count = connection.execute(
            text("SELECT COUNT(*) FROM sales_mart")
        ).scalar_one()

        if sales_count == 0:
            print("В sales_mart нет данных.")
            return

        print("Строк в sales_mart:", sales_count)

        # 6. Обновляем dim_products
        connection.execute(text("""
            INSERT INTO dim_products (
                product_id,
                product_name,
                category
            )
            SELECT DISTINCT ON (product_id)
                product_id,
                product_name,
                category
            FROM sales_mart
            ORDER BY product_id, created_at DESC

            ON CONFLICT (product_id)
            DO UPDATE SET
                product_name = EXCLUDED.product_name,
                category = EXCLUDED.category
        """))

        print("dim_products обновлена.")

        # 7. Обновляем dim_users
        connection.execute(text("""
            INSERT INTO dim_users (
                user_id,
                city,
                channel
            )
            SELECT DISTINCT ON (user_id)
                user_id,
                city,
                channel
            FROM sales_mart
            ORDER BY user_id, created_at DESC

            ON CONFLICT (user_id)
            DO UPDATE SET
                city = EXCLUDED.city,
                channel = EXCLUDED.channel
        """))

        print("dim_users обновлена.")

        # 8. Обновляем dim_date
        connection.execute(text("""
            INSERT INTO dim_date (
                date_id,
                full_date,
                day,
                month,
                year
            )
            SELECT DISTINCT
                TO_CHAR(created_at::date, 'YYYYMMDD')::INTEGER,
                created_at::date,
                EXTRACT(DAY FROM created_at)::INTEGER,
                EXTRACT(MONTH FROM created_at)::INTEGER,
                EXTRACT(YEAR FROM created_at)::INTEGER
            FROM sales_mart

            ON CONFLICT (date_id)
            DO UPDATE SET
                full_date = EXCLUDED.full_date,
                day = EXCLUDED.day,
                month = EXCLUDED.month,
                year = EXCLUDED.year
        """))

        print("dim_date обновлена.")

        # 9. Обновляем fact_sales
        connection.execute(text("""
            INSERT INTO fact_sales (
                order_id,
                product_id,
                user_id,
                date_id,
                quantity,
                unit_price,
                discount,
                revenue
            )
            SELECT
                order_id,
                product_id,
                user_id,
                TO_CHAR(created_at::date, 'YYYYMMDD')::INTEGER,
                quantity,
                unit_price,
                discount,
                revenue
            FROM sales_mart

            ON CONFLICT (order_id, product_id)
            DO UPDATE SET
                user_id = EXCLUDED.user_id,
                date_id = EXCLUDED.date_id,
                quantity = EXCLUDED.quantity,
                unit_price = EXCLUDED.unit_price,
                discount = EXCLUDED.discount,
                revenue = EXCLUDED.revenue
        """))

        print("fact_sales обновлена.")

        # 10. Проверяем результат
        for table in (
            "dim_products",
            "dim_users",
            "dim_date",
            "fact_sales"
        ):
            count = connection.execute(
                text(f"SELECT COUNT(*) FROM {table}")
            ).scalar_one()

            print(f"{table}: {count} строк")

    print("Звёздная схема успешно обновлена!")

build_star_schema()