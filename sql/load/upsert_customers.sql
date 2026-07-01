INSERT INTO customers
(
    customer_id,
    first_name,
    last_name,
    email,
    phone,
    city,
    state,
    created_at,
    etl_load_time,
    job_name
)

SELECT
    customer_id,
    first_name,
    last_name,
    email,
    phone,
    city,
    state,
    created_at,
    etl_load_time,
    job_name

FROM stg_customers

ON CONFLICT (customer_id)

DO UPDATE SET

first_name = EXCLUDED.first_name,

last_name = EXCLUDED.last_name,

email = EXCLUDED.email,

phone = EXCLUDED.phone,

city = EXCLUDED.city,

state = EXCLUDED.state,

etl_load_time = EXCLUDED.etl_load_time,

job_name = EXCLUDED.job_name;