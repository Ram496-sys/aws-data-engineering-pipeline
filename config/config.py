import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# ----------------------------
# File Paths
# ----------------------------

INPUT_FILE = PROJECT_ROOT / "data" / "raw" / "customers.csv"

PROCESSED_PATH = PROJECT_ROOT / "data" / "processed" / "customers_clean.csv"

REJECTED_PATH = PROJECT_ROOT / "data" / "rejected" / "customers_rejected.csv"

JDBC_DRIVER = PROJECT_ROOT / "drivers" / "postgresql-42.7.12.jar"

# ----------------------------
# Database Configuration
# ----------------------------

DB_HOST = os.getenv("DB_HOST")

DB_PORT = os.getenv("DB_PORT")

DB_NAME = os.getenv("DB_NAME")

DB_USER = os.getenv("DB_USER")

DB_PASSWORD = os.getenv("DB_PASSWORD")

DB_URL = (
    f"jdbc:postgresql://{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# ----------------------------
# Tables
# ----------------------------

STAGING_TABLE = "stg_customers"

CUSTOMER_TABLE = "customers"

AUDIT_TABLE = "etl_audit"

WATERMARK_TABLE = "etl_watermark"

# ----------------------------
# ETL
# ----------------------------

JOB_NAME = os.getenv("JOB_NAME")