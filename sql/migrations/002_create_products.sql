CREATE TABLE IF NOT EXISTS products (
    product_id BIGINT PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    brand VARCHAR(50),
    price DECIMAL(10,2),
    active_flag BOOLEAN DEFAULT TRUE
);