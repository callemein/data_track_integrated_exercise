import json

# AWS related libs
import boto3
import awswrangler as wr


# AWS Related Libs

def file_to_s3(data, s3_bucket, s3_prefix, filepath="file.json"):
    s3 = boto3.resource("s3")
    s3object = s3.Object(f"{s3_bucket}", f"{s3_prefix}/{filepath}")

    s3object.put(Body=(bytes(data.encode("UTF-8"))))


def dataframe_to_s3(df, s3_bucket, s3_prefix, filepath="file.parquet"):
    # Storing data on Data Lake
    wr.s3.to_parquet(
        df=df, path=f"s3://{s3_bucket}/{s3_prefix}/{filepath}", dataset=False
    )