from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import sys

BUCKET_NAME = "om-crypto-intelligence-dev"


def create_spark():

    return (
        SparkSession.builder
        .appName("ValidateSilver")

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


def fail_if(condition, message):

    if condition:
        print(f"\n❌ DATA QUALITY FAILED: {message}\n")
        sys.exit(1)


def main():

    spark = create_spark()

    print("\nReading Silver Layer...\n")

    df = spark.read.parquet(
        f"s3a://{BUCKET_NAME}/silver/data/"
    )

    print(f"Total Records : {df.count()}")

    ##################################################
    # NULL CHECKS
    ##################################################

    fail_if(
        df.filter(col("coin").isNull()).count() > 0,
        "Null coin names found."
    )

    fail_if(
        df.filter(col("price_usd").isNull()).count() > 0,
        "Null prices found."
    )

    ##################################################
    # NEGATIVE VALUES
    ##################################################

    fail_if(
        df.filter(col("price_usd") <= 0).count() > 0,
        "Invalid price detected."
    )

    fail_if(
        df.filter(col("market_cap") <= 0).count() > 0,
        "Invalid market cap detected."
    )

    fail_if(
        df.filter(col("volume_24h") < 0).count() > 0,
        "Invalid volume detected."
    )

    ##################################################
    # DUPLICATES
    ##################################################

    duplicate_count = (

        df.groupBy(
            "coin",
            "year",
            "month",
            "day",
            "hour"
        )

        .count()

        .filter(col("count") > 1)

        .count()

    )

    print("\nDuplicate Records:\n")

    df.groupBy(
        "coin",
        "year",
        "month",
        "day",
        "hour"
    ).count().filter(
        col("count") > 1
    ).show(100, False)

    fail_if(
        duplicate_count > 0,
        "Duplicate coins detected."
    )

    ##################################################

    print("\n✅ DATA QUALITY CHECKS PASSED\n")

    spark.stop()


if __name__ == "__main__":
    main()