from pathlib import Path
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import os
import sys

os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_FILE=PROJECT_ROOT / "data" / "raw" / "customers.csv"

spark=(SparkSession.builder.appName("Customer ETL").master("local[*]").getOrCreate())

df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(str(INPUT_FILE))
)

valid_df= df.filter(
    col("customer_id").isNotNull() &
    col("first_name").isNotNull() &
    col("email").isNotNull() 
)

invalid_df=df.filter(
                    col("customer_id").isNull() | 
                     col("first_name").isNull() |
                     col("email").isNull()
                     )

print("=" * 50)
print("valiad records",valid_df.count())

print("=" * 50)
print("Invalid records",invalid_df.count())

spark.stop()