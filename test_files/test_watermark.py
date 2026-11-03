from pathlib import Path
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

PROJECT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_DIR / ".env")

connection_url = (
    f"postgresql+psycopg://"
    f"{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}"
    f"/{os.getenv('DB_NAME')}"
)

engine = create_engine(connection_url)

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

    print("Watermark:", last_order_id)