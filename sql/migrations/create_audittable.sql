CREATE TABLE IF NOT EXISTS etl_audit (

    batch_id SERIAL PRIMARY KEY,

    job_name VARCHAR(100),

    records_read INT,

    records_loaded INT,

    records_rejected INT,

    status VARCHAR(20),

    start_time TIMESTAMP,

    end_time TIMESTAMP,

    duration INTERVAL
);