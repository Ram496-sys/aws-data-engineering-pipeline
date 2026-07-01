from pyspark.sql.functions import col, lit


def validate_duplicates(df):

    duplicate_emails = (
        df.groupBy("email")
        .count()
        .filter(col("count") > 1)
        .select("email")
    )

    reject_df = (
        df.join(
            duplicate_emails,
            on="email",
            how="inner"
        )
        .withColumn(
            "reject_reason",
            lit("DUPLICATE_EMAIL")
        )
    )

    clean_df = df.join(
        duplicate_emails,
        on="email",
        how="left_anti"
    )

    return clean_df, reject_df