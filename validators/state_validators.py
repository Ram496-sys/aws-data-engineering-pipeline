from pyspark.sql.functions import col, lit

VALID_STATES = [
    "Maharashtra",
    "Karnataka",
    "Goa",
    "Punjab",
    "Gujarat",
    "Tamil Nadu",
    "Kerala",
    "Telangana",
    "Odisha",
    "Rajasthan",
    "Assam",
    "Nagaland",
    "Jharkhand",
    "Manipur",
    "Himachal Pradesh",
]


def validate_state(df):

    reject_df = (
        df.filter(
            ~col("state").isin(VALID_STATES)
        )
        .withColumn(
            "reject_reason",
            lit("INVALID_STATE")
        )
    )

    clean_df = df.subtract(
        reject_df.drop("reject_reason")
    )

    return clean_df, reject_df