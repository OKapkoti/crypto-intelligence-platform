from pyspark.sql import SparkSession
import builtins
from pyspark.sql.functions import (
    col,
    count,
    sum,
    avg,
    max as spark_max,
    current_date,
    hour,
    to_date,
    current_timestamp
)

BUCKET_NAME = "om-crypto-intelligence-dev"


def create_spark():

    return (
        SparkSession.builder
        .appName("SilverToGold")

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


def write_dataset(df, path):

    (
        df.coalesce(1)
        .write
        .mode("append")
        .partitionBy(
            "snapshot_date",
            "snapshot_hour"
        )
        .parquet(path)
    )


def main():

    spark = create_spark()

    print("\nReading Silver Layer...\n")

    import boto3

    session = boto3.Session(profile_name="crypto-project")
    s3 = session.client("s3")

    response = s3.list_objects_v2(
        Bucket=BUCKET_NAME,
        Prefix="silver/data/"
    )

    folders = []

    folders = []

    latest_file = builtins.max(
        [
            obj
            for obj in response.get("Contents", [])
            if obj["Key"].endswith(".parquet")
        ],
        key=lambda obj: obj["LastModified"]
    )

    latest_partition = latest_file["Key"].rsplit("/", 1)[0]

    print(f"\nReading latest partition:\n{latest_partition}\n")

    silver_df = spark.read.parquet(
        f"s3a://{BUCKET_NAME}/{latest_partition}"
    )

    silver_df = (
        silver_df
        .withColumn(
            "snapshot_date",
            to_date("timestamp")
        )
        .withColumn(
            "snapshot_hour",
            hour("timestamp")
        )
    )

    print("\nSilver Schema:\n")
    silver_df.printSchema()

    ##################################################
    # TOP MARKET CAP
    ##################################################

    top_market_cap = (
        silver_df
        .orderBy(
            col("market_cap").desc()
        )
        .limit(10)
    )

    print("\nTop Market Cap\n")

    top_market_cap.show(truncate=False)

    write_dataset(
        top_market_cap,
        f"s3a://{BUCKET_NAME}/gold/top_market_cap/"
    )

    ##################################################
    # TOP GAINERS
    ##################################################

    top_gainers = (
        silver_df
        .orderBy(
            col("change_24h").desc()
        )
        .limit(10)
    )

    print("\nTop Gainers\n")

    top_gainers.show(truncate=False)

    write_dataset(
        top_gainers,
        f"s3a://{BUCKET_NAME}/gold/top_gainers/"
    )

    ##################################################
    # TOP LOSERS
    ##################################################

    top_losers = (
        silver_df
        .orderBy(
            col("change_24h").asc()
        )
        .limit(10)
    )

    print("\nTop Losers\n")

    top_losers.show(truncate=False)

    write_dataset(
        top_losers,
        f"s3a://{BUCKET_NAME}/gold/top_losers/"
    )

    ##################################################
    # HIGHEST VOLUME
    ##################################################

    highest_volume = (
        silver_df
        .orderBy(
            col("volume_24h").desc()
        )
        .limit(10)
    )

    print("\nHighest Volume\n")

    highest_volume.show(truncate=False)

    write_dataset(
        highest_volume,
        f"s3a://{BUCKET_NAME}/gold/highest_volume/"
    )

    ##################################################
    # MARKET SUMMARY
    ##################################################

    market_summary = (
        silver_df
        .agg(

            count("*").alias("total_coins"),

            sum("market_cap").alias(
                "total_market_cap"
            ),

            sum("volume_24h").alias(
                "total_volume_24h"
            ),

            avg("price_usd").alias(
                "average_price"
            ),

            spark_max("timestamp").alias(
                "snapshot_time"
            )

        )
    )

    market_summary = (
        market_summary
        .withColumn(
            "snapshot_date",
            to_date("snapshot_time")
        )
        .withColumn(
            "snapshot_hour",
            hour("snapshot_time")
        )
    )

    print("\nMarket Summary\n")

    market_summary.show(truncate=False)

    write_dataset(
        market_summary,
        f"s3a://{BUCKET_NAME}/gold/market_summary/"
    )
    ##################################################
    # COIN HISTORY
    ##################################################

    coin_history = (
        silver_df.select(
            "timestamp",
            "coin",
            "price_usd",
            "market_cap",
            "volume_24h",
            "change_24h",
            "snapshot_date",
            "snapshot_hour"
        )
    )

    print("\nCoin History\n")

    coin_history.show(truncate=False)

    write_dataset(
        coin_history,
        f"s3a://{BUCKET_NAME}/gold/coin_history/"
    )
    print("\nGold Layer Created Successfully!")

    spark.stop()


if __name__ == "__main__":
    main()