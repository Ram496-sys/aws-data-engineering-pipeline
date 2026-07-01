from config.config import (
    DB_URL,
    DB_USER,
    DB_PASSWORD,
    STAGING_TABLE,
)
from utils.logger import logger


def load_postgres(df):

    (
        df.write
        .format("jdbc")
        .option("url", DB_URL)
        .option("dbtable", STAGING_TABLE)
        .option("user", DB_USER)
        .option("password", DB_PASSWORD)
        .option("driver", "org.postgresql.Driver")
        .mode("overwrite")
        .save()
    )

    logger.info("Data loaded into PostgreSQL staging table.")