import json

import requests

# Source Related Libs

API_URL = "https://geo.irceline.be/sos/api/v1/"


def api_request(path, data=None, query=None, method="get"):
    resp = None

    query_string = ""
    if query is not None:
        query_string = "&".join([f"{key}={value}" for key, value in query.items()])

    if method == "post":
        resp = requests.post(f"{API_URL}/{path}?{query_string}", json=data)
    elif method == "get":
        resp = requests.get(f"{API_URL}/{path}?{query_string}")

    return resp.json()


def load_categories():
    categories = api_request("categories")
    return categories


def load_stations():
    stations = api_request("stations", query={"expanded": "true"})
    return stations


def load_timeseries_list():
    timeseries_list = api_request(
        "timeseries", query={"expanded": "true"}, method="get"
    )
    return timeseries_list


def load_datapoints_by_date(date, timeseries_ids):
    # Transform the timeseries_ids to a payload
    payload = {"timespan": f"{date}T00:00:00+02:00/PT24h", "timeseries": timeseries_ids}

    timeseries = api_request(f"timeseries/getData", data=payload, method="post")
    return timeseries
