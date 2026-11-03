
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Загружаем настройки из .env
load_dotenv()

# Формируем параметры подключения
connection_url = (
    f"postgresql+psycopg://"
    f"{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}"
    f"/{os.getenv('DB_NAME')}"
)

# Создаём движок SQLAlchemy
engine = create_engine(connection_url)

# Проверяем подключение
with engine.connect() as connection:
    result = connection.execute(text("SELECT version()"))
    print("Подключение успешно!")
    print(result.scalar())
