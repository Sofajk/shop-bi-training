CREATE TABLE IF NOT EXISTS sales_mart (
    order_id INTEGER PRIMARY KEY,
    created_at TIMESTAMP NOT NULL,
    user_id INTEGER NOT NULL,
    city VARCHAR(100),
    channel VARCHAR(50),
    product_name VARCHAR(150),
    category VARCHAR(100),
    quantity INTEGER NOT NULL,
    unit_price NUMERIC(12, 2) NOT NULL,
    discount NUMERIC(12, 2) DEFAULT 0,
    revenue NUMERIC(12, 2) NOT NULL
);

CREATE TABLE IF NOT EXISTS staging_sales_mart (
    order_id INTEGER,
    created_at TIMESTAMP,
    user_id INTEGER,
    city VARCHAR(100),
    channel VARCHAR(50),
    product_name VARCHAR(150),
    category VARCHAR(100),
    quantity INTEGER,
    unit_price NUMERIC(12, 2),
    discount NUMERIC(12, 2),
    revenue NUMERIC(12, 2)
);

CREATE TABLE IF NOT EXISTS etl_watermarks (
    pipeline_name VARCHAR(100) PRIMARY KEY,
    last_order_id INTEGER NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE sales_mart
ADD COLUMN product_id INTEGER;

ALTER TABLE staging_sales_mart
ADD COLUMN product_id INTEGER;

CREATE TABLE fact_sales (
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    date_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price NUMERIC(12, 2) NOT NULL,
    discount NUMERIC(12, 2) DEFAULT 0,
    revenue NUMERIC(12, 2) NOT NULL,
    CONSTRAINT fk_product
        FOREIGN KEY (product_id)
        REFERENCES dim_products(product_id),
    CONSTRAINT fk_user
        FOREIGN KEY (user_id)
        REFERENCES dim_users(user_id),
    CONSTRAINT fk_date
        FOREIGN KEY (date_id)
        REFERENCES dim_date(date_id),
    PRIMARY KEY (order_id, product_id)
);

CREATE TABLE dim_products (
    product_id INTEGER PRIMARY KEY,
    product_name VARCHAR(150),
    category VARCHAR(100)
);

CREATE TABLE dim_users (
    user_id INTEGER PRIMARY KEY,
    city VARCHAR(100),
    channel VARCHAR(50)
);

CREATE TABLE dim_date (
    date_id INTEGER PRIMARY KEY,
    full_date DATE UNIQUE,
    day INTEGER,
    month INTEGER,
    year INTEGER
);