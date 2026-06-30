import os
import sys
from pathlib import Path

# ----------------------------------------------------
# Fix PySpark Python Path
# ----------------------------------------------------

os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# ----------------------------------------------------
# Project Paths
# ----------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = PROJECT_ROOT / "data" / "raw" / "customers.csv"

PROCESSED_PATH = PROJECT_ROOT / "data" / "processed" / "customers_clean.csv"

REJECTED_PATH = PROJECT_ROOT / "data" / "rejected" / "customers_rejected.csv"

# ----------------------------------------------------
# Spark Session
# ----------------------------------------------------

def create_spark():

    spark = (
        SparkSession.builder
        .appName("Customer ETL")
        .master("local[*]")
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("ERROR")

    return spark


# ----------------------------------------------------
# Read Customer CSV
# ----------------------------------------------------

def read_customers(spark):

    print("\nReading Customer File...\n")

    df = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(str(INPUT_FILE))
    )

    return df


# ----------------------------------------------------
# NULL Validation
# ----------------------------------------------------

def validate_nulls(df):

    print("Running NULL Validation...\n")

    valid_df = df.filter(
        col("customer_id").isNotNull()
        & col("first_name").isNotNull()
        & col("email").isNotNull()
    )

    invalid_df = df.filter(
        col("customer_id").isNull()
        | col("first_name").isNull()
        | col("email").isNull()
    )

    return valid_df, invalid_df


# ----------------------------------------------------
# Duplicate Validation
# ----------------------------------------------------

def validate_duplicates(valid_df):

    print("Checking Duplicate Emails...\n")

    duplicate_df = (
        valid_df
        .groupBy("email")
        .count()
        .filter(col("count") > 1)
    )

    return duplicate_df


# ----------------------------------------------------
# Write Output
# (Temporary Local Solution)
# ----------------------------------------------------

def write_output(valid_df, invalid_df):

    PROCESSED_PATH.parent.mkdir(parents=True, exist_ok=True)
    REJECTED_PATH.parent.mkdir(parents=True, exist_ok=True)

    valid_df.toPandas().to_csv(PROCESSED_PATH, index=False)

    invalid_df.toPandas().to_csv(REJECTED_PATH, index=False)


# ----------------------------------------------------
# Metrics
# ----------------------------------------------------

def print_metrics(df, valid_df, invalid_df, duplicate_df):

    print("\n" + "=" * 60)

    print("ETL JOB SUMMARY")

    print("=" * 60)

    print(f"Total Records      : {df.count()}")

    print(f"Valid Records      : {valid_df.count()}")

    print(f"Invalid Records    : {invalid_df.count()}")

    print(f"Duplicate Emails   : {duplicate_df.count()}")

    print("=" * 60)


# ----------------------------------------------------
# Main ETL
# ----------------------------------------------------

def main():

    spark = create_spark()

    try:

        df = read_customers(spark)

        valid_df, invalid_df = validate_nulls(df)

        duplicate_df = validate_duplicates(valid_df)

        write_output(valid_df, invalid_df)

        print_metrics(
            df,
            valid_df,
            invalid_df,
            duplicate_df
        )

        print("\nDuplicate Email Report\n")

        duplicate_df.show(truncate=False)

        print("\nCustomer ETL Completed Successfully")

    except Exception as e:

        print("\nCustomer ETL Failed")

        print(e)

    finally:

        spark.stop()


if __name__ == "__main__":
    main()