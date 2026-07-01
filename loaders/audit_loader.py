import psycopg2
from datetime import datetime
from config.config import DB_USER, DB_PASSWORD
from utils.logger import logger


def insert_audit(
    records_read,
    records_loaded,
    records_rejected,
    status,
    start_time,
    end_time,
):

    conn = psycopg2.connect(
        host="localhost",
        database="enterprise_sales_db",
        user=DB_USER,
        password=DB_PASSWORD,
    )

    cur = conn.cursor()

    duration = end_time - start_time

    cur.execute(
        """
        INSERT INTO etl_audit
        (
            job_name,
            records_read,
            records_loaded,
            records_rejected,
            status,
            start_time,
            end_time,
            duration
        )

        VALUES
        (%s,%s,%s,%s,%s,%s,%s,%s)
        """,
        (
            "Customer ETL",
            records_read,
            records_loaded,
            records_rejected,
            status,
            start_time,
            end_time,
            duration,
        ),
    )

    conn.commit()

    cur.close()
    conn.close()

    logger.info("ETL audit record inserted.")