import boto3
from datetime import datetime

PROFILE_NAME = "crypto-project"
BUCKET_NAME = "om-crypto-intelligence-dev"


def upload_test_file():

    session = boto3.Session(
        profile_name=PROFILE_NAME
    )

    s3 = session.client("s3")

    content = f"""
This is a test upload.

Timestamp:
{datetime.now()}
"""

    s3.put_object(
        Bucket=BUCKET_NAME,
        Key="bronze/test/test_file.txt",
        Body=content
    )

    print("File uploaded successfully!")


if __name__ == "__main__":
    upload_test_file()