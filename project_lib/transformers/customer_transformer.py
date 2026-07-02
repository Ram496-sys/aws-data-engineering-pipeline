from pyspark.sql.functions import (
    initcap,
    lower,
    trim,
    current_timestamp,
    lit,
    col,
)


def transform_customer(df):

    return (
        df.withColumn(
            "first_name",
            initcap(trim(col("first_name")))
        )
        .withColumn(
            "last_name",
            initcap(trim(col("last_name")))
        )
        .withColumn(
            "email",
            lower(trim(col("email")))
        )
        .withColumn(
            "etl_load_time",
            current_timestamp()
        )
        .withColumn(
            "job_name",
            lit("Customer ETL")
        )
    )