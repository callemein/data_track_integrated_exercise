import sys
from time import sleep

import argparse
import logging


from datetime import datetime as dt

# import custom lib functions
from sinks import dataframe_to_s3

from sources import (
    load_datapoints_by_date,
    load_stations,
    load_categories,
    load_timeseries_list,
)

from transforms import (
    transform_stations_to_table,
    transform_categories_to_table,
    transform_timeseries_list_to_table,
    transform_datapoints_to_table,
)

s3_prefix = "timothy-data"

s3_stations_table = "stations.csv"
s3_timeseries_table = "timeseries.csv"
s3_categories_table = "categories.csv"

s3_datapoints_prefix = "data"
s3_datapoints_table = "data.csv"
s3_datapoints_compressed_table = "data.parquet"


def process_raw_data(s3_bucket: str, date: str):
    pass


def ingest_raw_stations(s3_bucket: str):
    stations = load_stations()
    stations_df = transform_stations_to_table(stations)
    dataframe_to_s3(stations_df, s3_bucket, s3_prefix, s3_stations_table)


def ingest_raw_categories(s3_bucket: str):
    categories = load_categories()
    categories_df = transform_categories_to_table(categories)
    dataframe_to_s3(categories_df, s3_bucket, s3_prefix, s3_categories_table)


def ingest_raw_timeseries_list(s3_bucket: str):
    timeseries_list = load_timeseries_list()
    timeseries_list_df = transform_timeseries_list_to_table(timeseries_list)
    dataframe_to_s3(timeseries_list_df, s3_bucket, s3_prefix, s3_timeseries_table)


def ingest_raw_datapoints(s3_bucket: str, date: str, compressed=True):
    timeseries_list = load_timeseries_list()
    timeseries_list_df = transform_timeseries_list_to_table(timeseries_list)

    date_object = dt.fromisoformat(date)
    # Filter all the timeseries with data available at the time
    available_timeseries = (timeseries_list_df["FIRST_VALUE_TIME"] < date_object) & (
        timeseries_list_df["LAST_VALUE_TIME"] >= date_object
    )

    # Get a list with all the relevant timeseries id's
    timeseries_ids = timeseries_list_df[available_timeseries]["TIMESERIES_ID"].tolist()

    datapoints = load_datapoints_by_date(date, timeseries_ids)
    datapoints_df = transform_datapoints_to_table(datapoints)

    if compressed:
        dataframe_to_s3(
            datapoints_df,
            s3_bucket,
            s3_prefix,
            f"{s3_datapoints_prefix}/{date}/{s3_datapoints_compressed_table}",
        )
    else:
        dataframe_to_s3(
            datapoints_df,
            s3_bucket,
            s3_prefix,
            f"{s3_datapoints_prefix}/{date}/{s3_datapoints_table}",
        )


def main():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    parser = argparse.ArgumentParser(description="Building greeter")
    parser.add_argument(
        "-d", "--date", dest="date", help="date in format YYYY-mm-dd", required=False
    )

    parser.add_argument(
        "-t",
        "--table",
        dest="table",
        help="The table you want to ingest: [categories, stations, data_points]",
        default="data_points",
    )

    parser.add_argument(
        "-b", "--bucket", dest="bucket", help="bucket name", required=True
    )

    args = parser.parse_args()
    logging.info(f"Using args: {args}")

    ingest_table = args.table
    if ingest_table == "categories":
        ingest_raw_categories(args.bucket)

    elif ingest_table == "stations":
        ingest_raw_stations(args.bucket)

    elif ingest_table == "timeseries":
        ingest_raw_timeseries_list(args.bucket)

    elif ingest_table == "data_points":
        ingest_raw_datapoints(args.bucket, args.date)

    else:
        print(
            "Please choose correct answer: [categories, stations, timeseries, data_points]"
        )


if __name__ == "__main__":
    main()
