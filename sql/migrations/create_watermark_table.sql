CREATE TABLE IF NOT EXISTS etl_watermark (

    job_name VARCHAR(100) PRIMARY KEY,

    last_customer_id BIGINT,

    last_run TIMESTAMP
);