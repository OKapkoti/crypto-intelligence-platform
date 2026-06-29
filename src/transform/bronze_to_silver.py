import boto3
from botocore.exceptions import ClientError
from pyspark.sql import SparkSession

from pyspark.sql.functions import (
    col,
    to_timestamp,
    year,
    month,
    dayofmonth,
    hour,
    current_timestamp
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

def partition_exists(timestamp):

    session = boto3.Session(
        profile_name=PROFILE_NAME
    )

    s3 = session.client("s3")

    prefix = (
        f"silver/data/"
        f"year={timestamp.year}/"
        f"month={timestamp.month}/"
        f"day={timestamp.day}/"
        f"hour={timestamp.hour}/"
    )

    response = s3.list_objects_v2(
        Bucket=BUCKET_NAME,
        Prefix=prefix
    )

    if "Contents" not in response:
        return False

    for obj in response["Contents"]:

        if obj["Key"].endswith(".parquet"):
            return True

    return False

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
            "timestamp",
            to_timestamp("timestamp")
        )
        .withColumn(
            "year",
            year("timestamp")
        )
        .withColumn(
            "month",
            month("timestamp")
        )
        .withColumn(
            "day",
            dayofmonth("timestamp")
        )
        .withColumn(
            "hour",
            hour("timestamp")
        )
    )

    print("\nTransformed Data:")
    df.show(truncate=False)

    from pyspark import StorageLevel

    df.persist(StorageLevel.MEMORY_AND_DISK)

    df.count()

    output_dir = "s3a://om-crypto-intelligence-dev/silver/data/"
    current_snapshot = df.select("timestamp").first()["timestamp"]

    print(f"\nCurrent Snapshot: {current_snapshot}")

    print("\nTesting Spark S3 write...")

    if partition_exists(current_snapshot):

        print("\n✅ Snapshot already processed. Skipping write.\n")

    else:

        (
            df.coalesce(1)
            .write
            .mode("append")
            .partitionBy(
                "year",
                "month",
                "day",
                "hour"
            )
            .parquet(output_dir)
        )

        print("\n✅ Spark S3 write successful")

    spark.stop()

    if os.path.exists(local_file):
        os.remove(local_file)


if __name__ == "__main__":
    main()