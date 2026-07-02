from pyspark.sql import SparkSession
from config.config import JDBC_DRIVER


def create_spark():

    spark = (
        SparkSession.builder
        .appName("Customer ETL")
        .master("local[*]")
        .config("spark.driver.extraClassPath", str(JDBC_DRIVER))
        .config("spark.executor.extraClassPath", str(JDBC_DRIVER))
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("ERROR")

    return spark