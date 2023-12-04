import sys

import argparse
import logging
import boto3

import json

from pyspark.sql import SparkSession
from pyspark.sql.functions import date_format, to_date, col, avg, from_utc_timestamp

# Settings
timezone = "Europe/Brussels"

aws_secret = "snowflake/integrated-exercise/timothy-login"

s3_prefix = "timothy-data"


def egress(bucket: str, date: str, sfOptions: dict):
    spark = (
        SparkSession.builder.config(
            "spark.jars.packages",
            ",".join(
                [
                    "org.apache.hadoop:hadoop-aws:3.3.1",
                    "net.snowflake:spark-snowflake_2.12:2.9.0-spark_3.1",
                    "net.snowflake:snowflake-jdbc:3.13.3",
                ]
            ),
        )
        .config(
            "spark.hadoop.fs.s3a.aws.credentials.provider",
            "com.amazonaws.auth.DefaultAWSCredentialsProviderChain",
        )
        .getOrCreate()
    )

    # DB files
    s3_table_data_points = (
        f"s3a://{bucket}/{s3_prefix}/clean/aggregate_station_by_day/{date}/*/*.parquet"
    )

    df = spark.read.parquet(s3_table_data_points)

    table_name = f"PPM_AVG_BY_STATIONS_{date.replace('-', '_')}"
    spark.sparkContext._jvm.net.snowflake.spark.snowflake.Utils.runQuery(
        sfOptions,
        f"""CREATE TABLE IF NOT EXISTS {table_name} (
        category_id INTEGER,
        category VARCHAR,
        timeseries_id INTEGER,
        station_name VARCHAR,
        date TIMESTAMP,
        avg_value DOUBLE)""",
    )

    df.write.format("snowflake").options(**sfOptions).option(
        "dbtable", f"{table_name}"
    ).mode("overwrite").save()


def get_snowflake_creds_from_sm(secret_name: str):
    sess = boto3.Session(region_name="eu-west-1")
    client = sess.client("secretsmanager")

    response = client.get_secret_value(SecretId=secret_name)

    creds = json.loads(response["SecretString"])
    return {
        "sfURL": f"{creds['URL']}",
        "sfPassword": creds["PASSWORD"],
        "sfUser": creds["USER_NAME"],
        "sfDatabase": creds["DATABASE"],
        "sfWarehouse": creds["WAREHOUSE"],
        "sfRole": creds["ROLE"],
        'sfSchema': creds['SCHEMA'],
    }


def main():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    parser = argparse.ArgumentParser(description="Building greeter")
    parser.add_argument(
        "-d", "--date", dest="date", help="date in format YYYY-mm-dd", required=True
    )

    parser.add_argument(
        "-b", "--bucket", dest="bucket", help="bucket name", required=True
    )

    args = parser.parse_args()
    logging.info(f"Using args: {args}")

    snowflake_creds = get_snowflake_creds_from_sm(aws_secret)
    egress(args.bucket, args.date, snowflake_creds)


if __name__ == "__main__":
    main()
