import sys

# =====================================================
# AWS GLUE IMPORTS (NEW)
# =====================================================
# CHANGED:
# Local SparkSession is replaced with GlueContext.

from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions

from pyspark.context import SparkContext
from pyspark.sql.functions import col

# =====================================================
# PROJECT IMPORTS (SAME)
# =====================================================

from validators.null_validators import validate_nulls
from validators.email_validators import validate_email
from validators.phone_validators import validate_phone
from validators.state_validators import validate_state
from validators.duplicate_validators import validate_duplicates

from transformers.customer_transformer import transform_customer

# =====================================================
# GLUE INITIALIZATION (NEW)
# =====================================================

args = getResolvedOptions(sys.argv, ["JOB_NAME"])

sc = SparkContext()

glueContext = GlueContext(sc)

spark = glueContext.spark_session

job = Job(glueContext)

job.init(args["JOB_NAME"], args)

# =====================================================
# S3 PATHS (CHANGED)
# =====================================================
# Local paths replaced with S3 locations

INPUT_FILE = "s3://ram-data-engineering-dev/raw/customers.csv"

PROCESSED_PATH = "s3://ram-data-engineering-dev/processed/"

REJECTED_PATH = "s3://ram-data-engineering-dev/rejected/"


# =====================================================
# WRITE OUTPUT (CHANGED)
# =====================================================
# OLD:
# clean_df.toPandas().to_csv(...)
#
# NEW:
# Spark writes directly to S3


def write_output(clean_df, reject_df):

    clean_df.write \
        .mode("overwrite") \
        .option("header", True) \
        .csv(PROCESSED_PATH)

    reject_df.write \
        .mode("overwrite") \
        .option("header", True) \
        .csv(REJECTED_PATH)


# =====================================================
# METRICS (SAME)
# =====================================================

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


# =====================================================
# MAIN ETL
# =====================================================

def main():

    print("Starting AWS Glue Customer ETL...\n")

    # =================================================
    # READ FROM S3 (CHANGED)
    # =================================================

    df = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(INPUT_FILE)
    )

    total_records = df.count()

    # =================================================
    # VALIDATIONS (UNCHANGED)
    # =================================================

    clean_df, null_reject = validate_nulls(df)

    clean_df, email_reject = validate_email(clean_df)

    clean_df, phone_reject = validate_phone(clean_df)

    clean_df, state_reject = validate_state(clean_df)

    clean_df, duplicate_reject = validate_duplicates(clean_df)

    # =================================================
    # MERGE REJECTED (UNCHANGED)
    # =================================================

    reject_df = (
        null_reject
        .unionByName(email_reject)
        .unionByName(phone_reject)
        .unionByName(state_reject)
        .unionByName(duplicate_reject)
    )

    # =================================================
    # TRANSFORMATION (UNCHANGED)
    # =================================================

    clean_df = transform_customer(clean_df)

    # =================================================
    # WRITE TO S3 (CHANGED)
    # =================================================

    write_output(clean_df, reject_df)

    # =================================================
    # METRICS
    # =================================================

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

    # =================================================
    # GLUE COMMIT (NEW)
    # =====================================================

    job.commit()

    print("\nAWS Glue ETL Completed Successfully")


# =====================================================
# START
# =====================================================

if __name__ == "__main__":
    main()