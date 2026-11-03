from datetime import date, datetime, timedelta
from typing import Optional
from fastapi import FastAPI, HTTPException, Query

app = FastAPI(
    title="Shop BI Training API",
    description="Учебный API интернет-магазина для практики BI, ETL и SQL. Все данные вымышлены.",
    version="1.0.0",
)

users = [
    {"user_id": 1001, "registered_at": "2025-11-02", "city": "Москва", "channel": "organic"},
    {"user_id": 1002, "registered_at": "2025-11-05", "city": "Санкт-Петербург", "channel": "paid_search"},
    {"user_id": 1003, "registered_at": "2025-12-12", "city": "Казань", "channel": "social"},
    {"user_id": 1004, "registered_at": "2026-01-03", "city": "Москва", "channel": "referral"},
    {"user_id": 1005, "registered_at": "2026-01-18", "city": "Екатеринбург", "channel": "organic"},
    {"user_id": 1006, "registered_at": "2026-02-09", "city": "Новосибирск", "channel": "paid_search"},
    {"user_id": 1007, "registered_at": "2026-03-14", "city": "Санкт-Петербург", "channel": "email"},
    {"user_id": 1008, "registered_at": "2026-04-21", "city": "Москва", "channel": "social"},
    {"user_id": 1009, "registered_at": "2026-05-10", "city": "Самара", "channel": "organic"},
    {"user_id": 1010, "registered_at": "2026-06-01", "city": "Казань", "channel": "paid_search"},
    {"user_id": 1011, "registered_at": "2026-06-17", "city": "Москва", "channel": "referral"},
    {"user_id": 1012, "registered_at": "2026-07-04", "city": "Краснодар", "channel": "social"},
]

products = [
    {"product_id": 201, "product_name": "Беспроводные наушники", "category": "Электроника", "unit_price": 5990.00},
    {"product_id": 202, "product_name": "Механическая клавиатура", "category": "Электроника", "unit_price": 7490.00},
    {"product_id": 203, "product_name": "Термокружка", "category": "Дом", "unit_price": 1290.00},
    {"product_id": 204, "product_name": "Рюкзак городской", "category": "Аксессуары", "unit_price": 3990.00},
    {"product_id": 205, "product_name": "Настольная лампа", "category": "Дом", "unit_price": 2490.00},
    {"product_id": 206, "product_name": "Фитнес-браслет", "category": "Электроника", "unit_price": 4290.00},
    {"product_id": 207, "product_name": "Бутылка для воды", "category": "Аксессуары", "unit_price": 890.00},
    {"product_id": 208, "product_name": "Подставка для ноутбука", "category": "Электроника", "unit_price": 2190.00},
]

orders = [
    {"order_id": 5001, "user_id": 1001, "product_id": 201, "quantity": 1, "unit_price": 5990.00, "discount": 0.00, "status": "paid", "created_at": "2026-10-01T09:15:00"},
    {"order_id": 5002, "user_id": 1002, "product_id": 203, "quantity": 2, "unit_price": 1290.00, "discount": 100.00, "status": "paid", "created_at": "2026-10-01T12:42:00"},
    {"order_id": 5003, "user_id": 1003, "product_id": 202, "quantity": 1, "unit_price": 7490.00, "discount": 500.00, "status": "paid", "created_at": "2026-10-02T15:30:00"},
    {"order_id": 5004, "user_id": 1001, "product_id": 204, "quantity": 1, "unit_price": 3990.00, "discount": 0.00, "status": "shipped", "created_at": "2026-10-03T10:05:00"},
    {"order_id": 5005, "user_id": 1004, "product_id": 205, "quantity": 1, "unit_price": 2490.00, "discount": 200.00, "status": "paid", "created_at": "2026-10-03T18:21:00"},
    {"order_id": 5006, "user_id": 1005, "product_id": 206, "quantity": 1, "unit_price": 4290.00, "discount": 0.00, "status": "cancelled", "created_at": "2026-10-04T11:08:00"},
    {"order_id": 5007, "user_id": 1006, "product_id": 207, "quantity": 3, "unit_price": 890.00, "discount": 100.00, "status": "paid", "created_at": "2026-10-05T08:45:00"},
    {"order_id": 5008, "user_id": 1007, "product_id": 208, "quantity": 1, "unit_price": 2190.00, "discount": 0.00, "status": "refunded", "created_at": "2026-10-05T19:11:00"},
    {"order_id": 5009, "user_id": 1008, "product_id": 201, "quantity": 2, "unit_price": 5790.00, "discount": 300.00, "status": "paid", "created_at": "2026-10-06T13:24:00"},
    {"order_id": 5010, "user_id": 1009, "product_id": 203, "quantity": 1, "unit_price": 1290.00, "discount": 0.00, "status": "paid", "created_at": "2026-10-07T09:02:00"},
    {"order_id": 5011, "user_id": 1010, "product_id": 202, "quantity": 1, "unit_price": 7490.00, "discount": 0.00, "status": "pending", "created_at": "2026-10-08T14:17:00"},
    {"order_id": 5012, "user_id": 1011, "product_id": 204, "quantity": 2, "unit_price": 3990.00, "discount": 400.00, "status": "paid", "created_at": "2026-10-09T16:40:00"},
    {"order_id": 5013, "user_id": 1012, "product_id": 205, "quantity": 1, "unit_price": 2490.00, "discount": 0.00, "status": "paid", "created_at": "2026-10-10T10:33:00"},
    {"order_id": 5014, "user_id": 1002, "product_id": 206, "quantity": 2, "unit_price": 4190.00, "discount": 500.00, "status": "paid", "created_at": "2026-10-11T20:02:00"},
    {"order_id": 5015, "user_id": 1003, "product_id": 207, "quantity": 1, "unit_price": 890.00, "discount": 0.00, "status": "cancelled", "created_at": "2026-10-12T12:11:00"},
    {"order_id": 5016, "user_id": 1004, "product_id": 208, "quantity": 2, "unit_price": 2190.00, "discount": 200.00, "status": "paid", "created_at": "2026-10-13T08:56:00"},
    {"order_id": 5017, "user_id": 1005, "product_id": 201, "quantity": 1, "unit_price": 5990.00, "discount": 500.00, "status": "paid", "created_at": "2026-10-14T17:25:00"},
    {"order_id": 5018, "user_id": 1006, "product_id": 203, "quantity": 4, "unit_price": 1290.00, "discount": 300.00, "status": "paid", "created_at": "2026-10-15T11:48:00"},
    {"order_id": 5019, "user_id": 1007, "product_id": 204, "quantity": 1, "unit_price": 3990.00, "discount": 0.00, "status": "shipped", "created_at": "2026-10-16T14:09:00"},
    {"order_id": 5020, "user_id": 1008, "product_id": 206, "quantity": 1, "unit_price": 4290.00, "discount": 0.00, "status": "paid", "created_at": "2026-10-17T10:01:00"},
    {"order_id": 5021, "user_id": 1009, "product_id": 202, "quantity": 1, "unit_price": 7490.00, "discount": 0.00, "status": "paid", "created_at": "2026-10-18T18:30:00"},
    {"order_id": 5022, "user_id": 1010, "product_id": 207, "quantity": 2, "unit_price": 890.00, "discount": 100.00, "status": "paid", "created_at": "2026-10-19T09:44:00"},
    {"order_id": 5023, "user_id": 1011, "product_id": 205, "quantity": 1, "unit_price": 2490.00, "discount": 0.00, "status": "pending", "created_at": "2026-10-20T13:12:00"},
    {"order_id": 5024, "user_id": 1012, "product_id": 201, "quantity": 1, "unit_price": 5990.00, "discount": 0.00, "status": "paid", "created_at": "2026-10-21T15:37:00"},
    {"order_id": 5025, "user_id": 1001, "product_id": 208, "quantity": 1, "unit_price": 2190.00, "discount": 100.00, "status": "paid", "created_at": "2026-10-22T08:27:00"},
    {"order_id": 5026, "user_id": 1002, "product_id": 204, "quantity": 1, "unit_price": 3990.00, "discount": 0.00, "status": "refunded", "created_at": "2026-10-23T19:55:00"},
    {"order_id": 5027, "user_id": 1003, "product_id": 203, "quantity": 2, "unit_price": 1290.00, "discount": 100.00, "status": "paid", "created_at": "2026-10-24T12:03:00"},
    {"order_id": 5028, "user_id": 1004, "product_id": 206, "quantity": 1, "unit_price": 4290.00, "discount": 0.00, "status": "paid", "created_at": "2026-10-25T10:49:00"},
    {"order_id": 5029, "user_id": 1005, "product_id": 202, "quantity": 1, "unit_price": 7490.00, "discount": 500.00, "status": "paid", "created_at": "2026-10-26T16:22:00"},
    {"order_id": 5030, "user_id": 1006, "product_id": 205, "quantity": 1, "unit_price": 2490.00, "discount": 0.00, "status": "paid", "created_at": "2026-10-27T09:38:00"},
    {"order_id": 5031, "user_id": 1001, "product_id": 201, "quantity": 1, "unit_price": 5990.00, "discount": 0.00, "status": "paid", "created_at": "2026-11-02T10:00:00"},
    {"order_id": 5032, "user_id": 1002, "product_id": 202, "quantity": 1, "unit_price": 7490.00, "discount": 500.00, "status": "paid", "created_at": "2026-11-02T10:15:00"},
    {"order_id": 5033, "user_id": 1003, "product_id": 203, "quantity": 2, "unit_price": 1290.00, "discount": 100.00, "status": "paid", "created_at": "2026-11-02T10:30:00"},
    {"order_id": 5034, "user_id": 1004, "product_id": 204, "quantity": 1, "unit_price": 3990.00, "discount": 0.00, "status": "paid", "created_at": "2026-11-03T10:00:00"},
    {"order_id": 5035, "user_id": 1005, "product_id": 205, "quantity": 2, "unit_price": 2490.00, "discount": 300.00, "status": "paid", "created_at": "2026-11-03T11:30:00"},
    {"order_id": 5036, "user_id": 1002, "product_id": 202, "quantity": 1, "unit_price": 7490.00, "discount": 500.00, "status": "paid", "created_at": "2026-11-03T14:00:00"}
]

# Временные данные для тестирования пагинации
# test_orders = []
#
# for i in range(250):
#     test_orders.append({
#         "order_id": 6001 + i,
#         "user_id": 1001,
#         "product_id": 201,
#         "quantity": 1,
#         "unit_price": 5990.00,
#         "discount": 0.00,
#         "status": "paid",
#         "created_at": "2026-11-02T09:15:00"
#     })
#
# orders.extend(test_orders)

payments = [
    {"payment_id": 9001, "order_id": 5001, "paid_at": "2026-10-01T09:16:00", "amount": 5990.00, "payment_method": "card", "payment_status": "success"},
    {"payment_id": 9002, "order_id": 5002, "paid_at": "2026-10-01T12:43:00", "amount": 2480.00, "payment_method": "sbp", "payment_status": "success"},
    {"payment_id": 9003, "order_id": 5003, "paid_at": "2026-10-02T15:31:00", "amount": 6990.00, "payment_method": "card", "payment_status": "success"},
    {"payment_id": 9004, "order_id": 5005, "paid_at": "2026-10-03T18:22:00", "amount": 2290.00, "payment_method": "card", "payment_status": "success"},
    {"payment_id": 9005, "order_id": 5006, "paid_at": "2026-10-04T11:09:00", "amount": 4290.00, "payment_method": "card", "payment_status": "refunded"},
    {"payment_id": 9006, "order_id": 5007, "paid_at": "2026-10-05T08:46:00", "amount": 2570.00, "payment_method": "sbp", "payment_status": "success"},
    {"payment_id": 9007, "order_id": 5008, "paid_at": "2026-10-05T19:12:00", "amount": 2190.00, "payment_method": "card", "payment_status": "refunded"},
    {"payment_id": 9008, "order_id": 5009, "paid_at": "2026-10-06T13:25:00", "amount": 11280.00, "payment_method": "card", "payment_status": "success"},
    {"payment_id": 9009, "order_id": 5010, "paid_at": "2026-10-07T09:03:00", "amount": 1290.00, "payment_method": "cash", "payment_status": "success"},
    {"payment_id": 9010, "order_id": 5011, "paid_at": None, "amount": 7490.00, "payment_method": "card", "payment_status": "pending"},
    {"payment_id": 9011, "order_id": 5012, "paid_at": "2026-10-09T16:41:00", "amount": 7580.00, "payment_method": "card", "payment_status": "success"},
    {"payment_id": 9012, "order_id": 5013, "paid_at": "2026-10-10T10:34:00", "amount": 2490.00, "payment_method": "sbp", "payment_status": "success"},
    {"payment_id": 9013, "order_id": 5014, "paid_at": "2026-10-11T20:03:00", "amount": 7880.00, "payment_method": "card", "payment_status": "success"},
    {"payment_id": 9014, "order_id": 5015, "paid_at": "2026-10-12T12:12:00", "amount": 890.00, "payment_method": "card", "payment_status": "refunded"},
    {"payment_id": 9015, "order_id": 5016, "paid_at": "2026-10-13T08:57:00", "amount": 4180.00, "payment_method": "sbp", "payment_status": "success"},
    {"payment_id": 9016, "order_id": 5017, "paid_at": "2026-10-14T17:26:00", "amount": 5490.00, "payment_method": "card", "payment_status": "success"},
    {"payment_id": 9017, "order_id": 5018, "paid_at": "2026-10-15T11:49:00", "amount": 4860.00, "payment_method": "card", "payment_status": "success"},
    {"payment_id": 9018, "order_id": 5019, "paid_at": "2026-10-16T14:10:00", "amount": 3990.00, "payment_method": "cash", "payment_status": "success"},
    {"payment_id": 9019, "order_id": 5020, "paid_at": "2026-10-17T10:02:00", "amount": 4290.00, "payment_method": "card", "payment_status": "success"},
    {"payment_id": 9020, "order_id": 5021, "paid_at": "2026-10-18T18:31:00", "amount": 7490.00, "payment_method": "card", "payment_status": "success"},
]

def page(items, limit: int, offset: int):
    return {"total": len(items), "limit": limit, "offset": offset, "items": items[offset:offset + limit]}

@app.get("/")
def root():
    return {
        "message": "Shop BI Training API",
        "docs": "/docs",
        "endpoints": ["/users", "/products", "/orders", "/payments"],
        "note": "Все данные вымышлены и предназначены для обучения."
    }

@app.get("/users")
def get_users(city: Optional[str] = None, limit: int = Query(100, ge=1, le=100), offset: int = Query(0, ge=0)):
    data = users if city is None else [u for u in users if u["city"].lower() == city.lower()]
    return page(data, limit, offset)

@app.get("/products")
def get_products(category: Optional[str] = None, limit: int = Query(100, ge=1, le=100), offset: int = Query(0, ge=0)):
    data = products if category is None else [p for p in products if p["category"].lower() == category.lower()]
    return page(data, limit, offset)

@app.get("/orders")
def get_orders(
    status: Optional[str] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    order_id_from: Optional[int] = None,
    limit: int = Query(100, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    data = orders
    if status is not None:
        data = [o for o in data if o["status"].lower() == status.lower()]
    if date_from is not None:
        data = [o for o in data if date.fromisoformat(o["created_at"][:10]) >= date_from]
    if date_to is not None:
        data = [o for o in data if date.fromisoformat(o["created_at"][:10]) <= date_to]
    if order_id_from is not None:
        data = [o for o in data if o["order_id"] > order_id_from]

    return page(data, limit, offset)

@app.get("/payments")
def get_payments(
    payment_status: Optional[str] = None,
    limit: int = Query(100, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    data = payments
    if payment_status is not None:
        data = [p for p in data if p["payment_status"].lower() == payment_status.lower()]
    return page(data, limit, offset)

@app.get("/orders/{order_id}")
def get_order(order_id: int):
    for order in orders:
        if order["order_id"] == order_id:
            return order
    raise HTTPException(status_code=404, detail="Order not found")
