from pathlib import Path
from pyspark.sql import SparkSession

PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_FILE=PROJECT_ROOT / "data" / "raw" / "customer.csv"

spark=(SparkSession.builder.appName("Customer ETL").master("local[*]").getOrCreate())

df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(str(INPUT_FILE))
)

print("=" * 60)
print("Customer Dataset")
print("=" * 60)

df.show(10, truncate=False)

print("=" * 60)
print("Schema")
print("=" * 60)

df.printSchema()

spark.stop()