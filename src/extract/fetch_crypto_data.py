import requests
import boto3
import json

from datetime import datetime

PROFILE_NAME = "crypto-project"
BUCKET_NAME = "om-crypto-intelligence-dev"


def fetch_crypto_data():

    url = (
        "https://api.coingecko.com/api/v3/"
        "simple/price"
    )

    params = {
        "ids": "bitcoin,ethereum,solana,ripple,dogecoin",
        "vs_currencies": "usd",
        "include_market_cap": "true",
        "include_24hr_vol": "true",
        "include_24hr_change": "true"
    }

    response = requests.get(
        url,
        params=params,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    timestamp = datetime.utcnow().isoformat()

    records = []

    for coin, metrics in data.items():

        records.append({
            "timestamp": timestamp,
            "coin": coin,
            "price_usd": metrics.get("usd"),
            "market_cap": metrics.get("usd_market_cap"),
            "volume_24h": metrics.get("usd_24h_vol"),
            "change_24h": metrics.get("usd_24h_change")
        })

    return records


def upload_to_s3(records):

    session = boto3.Session(
        profile_name=PROFILE_NAME
    )

    s3 = session.client("s3")

    now = datetime.utcnow()

    file_name = now.strftime("crypto_%Y%m%d_%H%M%S.json")

    key = (
        f"bronze/"
        f"year={now.year}/"
        f"month={now.month:02d}/"
        f"day={now.day:02d}/"
        f"hour={now.hour:02d}/"
        f"{file_name}"
    )

    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=key,
        Body=json.dumps(records, indent=2)
    )

    print(f"Uploaded to S3: {key}")


if __name__ == "__main__":

    records = fetch_crypto_data()

    print("\nRecords Fetched:\n")

    print(json.dumps(records, indent=2))

    upload_to_s3(records)