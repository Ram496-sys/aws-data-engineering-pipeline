from pyspark.sql.functions import col, length, lit


def validate_phone(df):

    reject_df = (
        df.filter(
            length(col("phone").cast("string")) != 10
        )
        .withColumn(
            "reject_reason",
            lit("INVALID_PHONE")
        )
    )

    clean_df = df.subtract(
        reject_df.drop("reject_reason")
    )

    return clean_df, reject_df