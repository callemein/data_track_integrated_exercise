import sys
from time import sleep

import argparse
import requests
import logging

import boto3

import json

import awswrangler as wr
import pandas as pd

# import custom lib functions
from sinks import file_to_s3, dataframe_to_s3
from sources import load_station_timeseries, load_timeseries_by_date, load_stations

from transforms import (
    replace_ids_with_reference,
    transform_stations,
    create_map_timeseries_station,
)

s3_prefix = "timothy-data"


def process_raw_data(s3_bucket: str, date: str):
    pass


def ingest_raw_data_single(s3_bucket: str, date: str):
    stations = load_stations()
    stations = transform_stations(stations)

    for station_ref in stations:
        station = stations[station_ref]

        timeseries = load_station_timeseries(station["id"])

        timeseries_data = load_timeseries_by_date(date, list(timeseries.keys()))
        timeseries_data = replace_ids_with_reference(timeseries, timeseries_data)

        file_to_s3(
            json.dumps(timeseries_data),
            s3_bucket,
            f"{s3_prefix}/{date}",
            f"{station['id']}.json",
        )


def ingest_raw_data_bulk(s3_bucket: str, date: str):
    stations = load_stations()
    stations = transform_stations(stations)

    station_timeseries_map = {}
    timeseries_station_map = {}
    for station_ref in stations:
        station = stations[station_ref]

        timeseries = load_station_timeseries(station["id"])
        station_timeseries_map[station_ref] = timeseries
        timeseries_station_map.update(
            create_map_timeseries_station(station_ref, list(timeseries.keys()))
        )

    timeseries_data = load_timeseries_by_date(date, list(timeseries_station_map.keys()))

    station_data = {station_ref: {} for station_ref in stations}
    for id, data in timeseries_data.items():
        station_ref = timeseries_station_map[id]
        category_ref = station_timeseries_map[station_ref][id]
        station_data[station_ref][category_ref] = data

    for station_ref in stations:
        timeseries_data = station_data[station_ref]
        file_to_s3(
            json.dumps(timeseries_data),
            s3_bucket,
            f"{s3_prefix}/{date}",
            f"{station['id']}.json",
        )


def main():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    parser = argparse.ArgumentParser(description="Building greeter")
    parser.add_argument(
        "-d", "--date", dest="date", help="date in format YYYY-mm-dd", required=True
    )

    parser.add_argument(
        "-b", "--bucket", dest="bucket", help="bucket name", required=True
    )

    parser.add_argument(
        "-e",
        "--env",
        dest="env",
        help="The environment in which we execute the code",
        required=True,
    )

    parser.add_argument(
        "-ip",
        "--ingestion-proces",
        dest="ingestion_process",
        help="The ingestion process: [single, bulk]",
        required=True,
    )

    args = parser.parse_args()
    logging.info(f"Using args: {args}")

    if args.ingestion_process == "single":
        ingest_raw_data_single(args.bucket, args.date)
    else:
        ingest_raw_data_bulk(args.bucket, args.date)


if __name__ == "__main__":
    main()
