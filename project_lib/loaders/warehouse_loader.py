import psycopg2
from config.config import DB_USER, DB_PASSWORD


def update_warehouse():

    conn = psycopg2.connect(
        host="localhost",
        database="enterprise_sales_db",
        user=DB_USER,
        password=DB_PASSWORD,
    )

    cur = conn.cursor()

    with open("sql/load/upsert_customers.sql") as file:
        cur.execute(file.read())

    conn.commit()

    cur.close()
    conn.close()

    print("✅ Customers table updated")