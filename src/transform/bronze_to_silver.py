from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    to_timestamp,
    year,
    month,
    dayofmonth
)

import boto3
import tempfile
import os
import shutil

BUCKET_NAME = "om-crypto-intelligence-dev"
PROFILE_NAME = "crypto-project"


def create_spark():

    return (
        SparkSession.builder
        .appName("BronzeToSilver")

        .config(
            "spark.hadoop.fs.s3a.aws.credentials.provider",
            "com.amazonaws.auth.profile.ProfileCredentialsProvider"
        )

        .config(
            "spark.hadoop.fs.s3a.endpoint",
            "s3.ap-south-1.amazonaws.com"
        )

        .config(
            "spark.hadoop.fs.s3a.impl",
            "org.apache.hadoop.fs.s3a.S3AFileSystem"
        )

        .config(
            "spark.hadoop.fs.s3a.path.style.access",
            "true"
        )

        .getOrCreate()
    )


def get_latest_bronze_file():

    session = boto3.Session(
        profile_name=PROFILE_NAME
    )

    s3 = session.client("s3")

    response = s3.list_objects_v2(
        Bucket=BUCKET_NAME,
        Prefix="bronze/"
    )

    files = [
        obj["Key"]
        for obj in response.get("Contents", [])
        if obj["Key"].endswith(".json")
    ]

    latest_file = max(files)

    print(f"\nLatest Bronze File:")
    print(latest_file)

    return latest_file


def download_file(key):

    session = boto3.Session(
        profile_name=PROFILE_NAME
    )

    s3 = session.client("s3")

    local_file = os.path.join(
        tempfile.gettempdir(),
        "latest_crypto_data.json"
    )

    s3.download_file(
        BUCKET_NAME,
        key,
        local_file
    )

    return local_file


def main():

    spark = create_spark()

    latest_key = get_latest_bronze_file()

    local_file = download_file(latest_key)

    df = (
        spark.read
        .option("multiline", "true")
        .json(local_file)
    )

    df = (
        df
        .filter(col("coin").isNotNull())
        .filter(col("price_usd") > 0)
        .filter(col("market_cap") > 0)
        .filter(col("volume_24h") >= 0)
    )

    df = (
        df
        .withColumn(
            "event_timestamp",
            to_timestamp("timestamp")
        )
        .withColumn(
            "year",
            year("event_timestamp")
        )
        .withColumn(
            "month",
            month("event_timestamp")
        )
        .withColumn(
            "day",
            dayofmonth("event_timestamp")
        )
    )

    print("\nTransformed Data:")
    df.show(truncate=False)

    output_dir = "s3a://om-crypto-intelligence-dev/silver/data/"

    print("\nTesting Spark S3 write...")

    (
    df.coalesce(1)
    .write
    .mode("overwrite")
    .partitionBy(
        "year",
        "month",
        "day"
    )
    .parquet(
        "s3a://om-crypto-intelligence-dev/silver/data/"
    )
)
    print("\nSpark S3 write successful")

    spark.stop()

    if os.path.exists(local_file):
        os.remove(local_file)


if __name__ == "__main__":
    main()