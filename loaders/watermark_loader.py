import psycopg2
from config.config import DB_USER, DB_PASSWORD


def get_last_watermark():

    conn = psycopg2.connect(
        host="localhost",
        database="enterprise_sales_db",
        user=DB_USER,
        password=DB_PASSWORD,
    )

    cur = conn.cursor()

    cur.execute("""
        SELECT last_customer_id
        FROM etl_watermark
        WHERE job_name='Customer ETL'
    """)

    value = cur.fetchone()[0]

    cur.close()
    conn.close()

    return value

def update_watermark(customer_id):

    conn = psycopg2.connect(
        host="localhost",
        database="enterprise_sales_db",
        user=DB_USER,
        password=DB_PASSWORD,
    )

    cur = conn.cursor()

    cur.execute(
        """
        UPDATE etl_watermark

        SET

        last_customer_id=%s,

        last_run=CURRENT_TIMESTAMP

        WHERE job_name='Customer ETL'
        """,
        (customer_id,),
    )

    conn.commit()

    cur.close()
    conn.close()