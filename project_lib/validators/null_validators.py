from pyspark.sql.functions import col, lit


def validate_nulls(df):

    reject_df = (
        df.filter(
            col("customer_id").isNull()
            | col("first_name").isNull()
            | col("email").isNull()
        )
        .withColumn(
            "reject_reason",
            lit("NULL_VALIDATION")
        )
    )

    clean_df = df.subtract(
        reject_df.drop("reject_reason")
    )

    return clean_df, reject_df