CREATE TABLE IF NOT EXISTS customers (

    customer_id BIGINT PRIMARY KEY,

    first_name VARCHAR(100),

    last_name VARCHAR(100),

    email VARCHAR(255),

    phone VARCHAR(20),

    city VARCHAR(100),

    state VARCHAR(100),

    created_at TIMESTAMP,

    etl_load_time TIMESTAMP,

    job_name VARCHAR(100)

);