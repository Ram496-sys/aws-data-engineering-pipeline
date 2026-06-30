CREATE TABLE IF NOT EXISTS orders (
    order_id BIGINT PRIMARY KEY,
    customer_id BIGINT REFERENCES customers(customer_id),
    product_id BIGINT REFERENCES products(product_id),
    store_id INT REFERENCES stores(store_id),
    quantity INT NOT NULL,
    order_amount DECIMAL(10,2),
    order_date TIMESTAMP
)