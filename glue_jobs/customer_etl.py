import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

# -----------------------------------------------------
# Fix PySpark Python Path
# -----------------------------------------------------
os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

# -----------------------------------------------------
# Imports
# -----------------------------------------------------
from utils.spark_session import create_spark
from readers.csv_readers import read_csv

from validators.null_validators import validate_nulls
from validators.email_validators import validate_email
from validators.phone_validators import validate_phone
from validators.state_validators import validate_state
from validators.duplicate_validators import validate_duplicates

from transformers.customer_transformer import transform_customer
from loaders.postgres_loader import load_postgres
from loaders.warehouse_loader import update_warehouse
from datetime import datetime
from utils.logger import logger

from loaders.audit_loader import insert_audit
from loaders.watermark_loader import (
    get_last_watermark,
    update_watermark,
)

from pyspark.sql.functions import col, max

# -----------------------------------------------------
# Project Paths
# -----------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = PROJECT_ROOT / "data" / "raw" / "customers.csv"

PROCESSED_PATH = PROJECT_ROOT / "data" / "processed" / "customers_clean.csv"

REJECTED_PATH = PROJECT_ROOT / "data" / "rejected" / "customers_rejected.csv"

# -----------------------------------------------------
# Write Output
# -----------------------------------------------------

def write_output(clean_df, reject_df):

    PROCESSED_PATH.parent.mkdir(parents=True, exist_ok=True)
    REJECTED_PATH.parent.mkdir(parents=True, exist_ok=True)

    clean_df.toPandas().to_csv(PROCESSED_PATH, index=False)
    reject_df.toPandas().to_csv(REJECTED_PATH, index=False)


# -----------------------------------------------------
# Print Metrics
# -----------------------------------------------------

def print_metrics(
    total,
    clean,
    rejected,
    duplicate,
    nulls,
    email,
    phone,
    state,
):

    print("\n" + "=" * 60)
    print("CUSTOMER ETL SUMMARY")
    print("=" * 60)

    print(f"Total Records      : {total}")
    print(f"Clean Records      : {clean}")
    print(f"Rejected Records   : {rejected}")

    print("-" * 60)

    print(f"NULL Errors        : {nulls}")
    print(f"Email Errors       : {email}")
    print(f"Phone Errors       : {phone}")
    print(f"State Errors       : {state}")
    print(f"Duplicate Emails   : {duplicate}")

    print("=" * 60)


# -----------------------------------------------------
# Main ETL
# -----------------------------------------------------

def main():

    start_time = datetime.now()
    spark = create_spark()

    try:

        logger.info("Starting Customer ETL...\n")

        # -------------------------------
        # Read
        # -------------------------------

        df = read_csv(spark, INPUT_FILE)

        total_records = df.count()

        last_customer = get_last_watermark()

        logger.info(f"Last Watermark : {last_customer}")

        df = df.filter(
            col("customer_id") > last_customer
        )

        logger.info(f"New Records : {df.count()}")

        # -------------------------------
        # Validation
        # -------------------------------

        clean_df, null_reject = validate_nulls(df)

        clean_df, email_reject = validate_email(clean_df)

        clean_df, phone_reject = validate_phone(clean_df)

        clean_df, state_reject = validate_state(clean_df)

        clean_df, duplicate_reject = validate_duplicates(clean_df)

        # -------------------------------
        # Merge all rejected records
        # -------------------------------

        reject_df = (
            null_reject
            .unionByName(email_reject)
            .unionByName(phone_reject)
            .unionByName(state_reject)
            .unionByName(duplicate_reject)
        )

        # -------------------------------
        # Transform
        # -------------------------------

        clean_df = transform_customer(clean_df)
        load_postgres(clean_df)
        update_warehouse()
        max_customer = (
            clean_df
            .agg(max("customer_id"))
            .collect()[0][0]
        )

        if max_customer is not None:
            update_watermark(max_customer)
            logger.info(f"Watermark Updated : {max_customer}")
        else:
            print("No valid records. Watermark not updated.")

        end_time = datetime.now()
        insert_audit(
            records_read=df.count(),
            records_loaded=clean_df.count(),
            records_rejected=reject_df.count(),
            status="SUCCESS",
            start_time=start_time,
            end_time=end_time,
        )

        # -------------------------------
        # Write
        # -------------------------------

        write_output(clean_df, reject_df)

        # -------------------------------
        # Metrics
        # -------------------------------

        print_metrics(
            total=total_records,
            clean=clean_df.count(),
            rejected=reject_df.count(),
            duplicate=duplicate_reject.count(),
            nulls=null_reject.count(),
            email=email_reject.count(),
            phone=phone_reject.count(),
            state=state_reject.count(),
        )

        print("\nSample Clean Records\n")

        clean_df.show(10, truncate=False)

        print("\nSample Rejected Records\n")

        reject_df.show(10, truncate=False)

        logger.info("Customer ETL completed successfully.")

    except Exception as ex:

        print("\nCustomer ETL Failed\n")

        logger.exception("Customer ETL failed.")

    finally:

        spark.stop()


if __name__ == "__main__":
    main()