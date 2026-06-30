CREATE TABLE IF NOT EXISTS payments (
    payment_id BIGINT PRIMARY KEY,
    order_id BIGINT REFERENCES orders(order_id),
    payment_method VARCHAR(30),
    payment_status VARCHAR(30),
    payment_date TIMESTAMP
);