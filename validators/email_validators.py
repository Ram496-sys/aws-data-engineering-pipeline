from pyspark.sql.functions import col, lit


def validate_email(df):

    reject_df = (
        df.filter(
            (~col("email").contains("@"))
            | (~col("email").contains("."))
        )
        .withColumn(
            "reject_reason",
            lit("INVALID_EMAIL")
        )
    )

    clean_df = df.subtract(
        reject_df.drop("reject_reason")
    )

    return clean_df, reject_df