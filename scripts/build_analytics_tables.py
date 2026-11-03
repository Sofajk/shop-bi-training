import pandas as pd
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent

sales_mart = pd.read_csv(
    PROJECT_DIR / "data" / "processed" / "sales_mart.csv"
)

print("\n--- SALES MART ---")
print(sales_mart.head(10).to_string(index=False))


# Выручка по городам
city_stats = (
    sales_mart.groupby("city")
    .agg(
        orders_count=("order_id", "count"),
        revenue=("revenue", "sum"),
        customers_count=("user_id", "nunique")
    )
    .reset_index()
    .sort_values("revenue", ascending=False)
)

print("\n--- АНАЛИТИКА ПО ГОРОДАМ ---")
print(city_stats.to_string(index=False))


# Выручка по категориям
category_stats = (
    sales_mart.groupby("category")
    .agg(
        orders_count=("order_id", "count"),
        quantity_sold=("quantity", "sum"),
        revenue=("revenue", "sum")
    )
    .reset_index()
    .sort_values("revenue", ascending=False)
)

print("\n--- АНАЛИТИКА ПО КАТЕГОРИЯМ ---")
print(category_stats.to_string(index=False))


# Эффективность каналов привлечения
channel_stats = (
    sales_mart.groupby("channel")
    .agg(
        orders_count=("order_id", "count"),
        customers_count=("user_id", "nunique"),
        revenue=("revenue", "sum")
    )
    .reset_index()
    .sort_values("revenue", ascending=False)
)

# Средняя выручка на заказ
channel_stats["average_order_value"] = (
    channel_stats["revenue"] / channel_stats["orders_count"]
)

print("\n--- АНАЛИТИКА ПО КАНАЛАМ ---")
print(channel_stats.to_string(index=False))

product_stats = (
    sales_mart.groupby("product_name")
    .agg(
        orders_count = ('order_id', 'count'),
        quantity_sold=('quantity', 'sum'),
        revenue=('revenue', 'sum')
    )
    .reset_index()
    .sort_values("revenue", ascending=False)
)
print('\n--- АНАЛИТИКА ПО ПРОДУКТАМ ---')
print(product_stats.to_string(index=False))


# Сводная таблица: выручка по категориям и городам

pivot_revenue = pd.pivot_table(
    sales_mart,
    values="revenue",
    index="category",
    columns="city",
    aggfunc="sum",
    fill_value=0
)

print("\n--- ВЫРУЧКА ПО КАТЕГОРИЯМ И ГОРОДАМ ---")
print(pivot_revenue.to_string())

pivot_channel_revenue = pd.pivot_table(
    sales_mart,
    values='revenue',
    index = 'category',
    columns = 'channel',
    aggfunc = 'sum',
    fill_value=0
)

print('\n--- ВЫРУЧКА ПО КАТЕГОРИЯМ И КАНАЛАМ ---')
print(pivot_channel_revenue.to_string())

pivot_product_quantity = pd.pivot_table(
    sales_mart,
    values="quantity",
    index="product_name",
    columns="channel",
    aggfunc="sum",
    fill_value=0
)

print("\n--- КОЛИЧЕСТВО ПРОДАННЫХ ТОВАРОВ ПО КАНАЛАМ ---")
print(pivot_product_quantity.to_string())