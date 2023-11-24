import json

import requests

# Source Related Libs

API_URL = "https://geo.irceline.be/sos/api/v1/"


def api_request(path, data=None, method="get"):
    resp = None

    if method == "post":
        resp = requests.post(f"{API_URL}/{path}", json=data)
    elif method == "get":
        resp = requests.get(f"{API_URL}/{path}")

    return resp.json()


def load_categories():
    categories = api_request("categories")
    return categories


def load_stations():
    stations = api_request("stations")
    return stations


def load_features():
    features = api_request("features")
    return features


def load_station_timeseries(station_id):
    resp = api_request(f"stations/{station_id}")
    raw_station_timeseries = resp["properties"]["timeseries"]

    station_timeseries = {}
    for timeseries_id in raw_station_timeseries:
        station_timeseries[timeseries_id] = raw_station_timeseries[timeseries_id][
            "category"
        ]["label"]

    return station_timeseries


def load_timeseries_by_date(date, timeseries_ids):
    # Transform the timeseries_ids to a payload
    payload = {"timespan": f"PT24h/{date}", "timeseries": timeseries_ids}

    resp = api_request(f"timeseries/getData", data = payload, method="post")

    timeseries = {}
    for timeseries_id in timeseries_ids:
        timeseries[timeseries_id] = [tvp['value'] for tvp in resp[timeseries_id]['values']]

    return timeseries
