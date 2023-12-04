# transform functions
import pandas as pd
from datetime import datetime as dt

from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

## Pandas enabled transformers


# Example output of api call
# [{
# 	"properties": {
# 		"id": 1030,
# 		"label": "40AL01 - Linkeroever"
# 	},
# 	"geometry": {
# 		"coordinates": [
# 			4.385223684454717,
# 			51.23619419990248,
# 			"NaN"
# 		],
# 		"type": "Point"
# 	},
# 	"type": "Feature"
# },]
def transform_stations_to_table(stations):
    columns = ["STATION_ID", "STATION_NAME", "LONGITUDE", "LATITUDE", "CITY"]
    data = []

    geolocator = Nominatim(user_agent="datatrack-tca-ingest")
    reverse = RateLimiter(geolocator.reverse, min_delay_seconds=1)

    for station in stations:
        address = (
            reverse(
                (
                    station["geometry"]["coordinates"][1],
                    station["geometry"]["coordinates"][0],
                )
            )
            .raw["address"]
        )
        city = address.get("city", "") or  address.get("town", "")

        data.append(
            [
                station["properties"]["id"],
                station["properties"]["label"],
                station["geometry"]["coordinates"][0],
                station["geometry"]["coordinates"][1],
                city
            ]
        )
        # break

    return pd.DataFrame(data, columns=columns).convert_dtypes()


# Example output of api call
# [{
# 	"id": "482",
#   "label": "1,2-XYLENE O-XYLENE"
# },]
def transform_categories_to_table(categories):
    columns = ["CATEGORY_ID", "CATEGORY"]
    data = []
    for category in categories:
        data.append(
            [
                category["id"],
                category["label"],
            ]
        )

    return pd.DataFrame(data, columns=columns).convert_dtypes()


# [{
#     "id": "6522",
#     "label": "1,2-XYLENE O-XYLENE 6522 - btx, o-xyleen - procedure, 41B006 - Bruxelles (Parlement UE)",
#     "extras": [
#         "license"
#     ],
#     "uom": "µg/m³",
#     "station": {
#         "properties": {
#             "id": 1112,
#             "label": "41B006 - Bruxelles (Parlement UE)"
#         },
#         "geometry": {
#             "coordinates": [
#                 4.374388284562104,
#                 50.838640177166184,
#                 "NaN"
#             ],
#             "type": "Point"
#         },
#         "type": "Feature"
#     },
#     "referenceValues": [],
#     "firstValue": {
#         "timestamp": 1338296400000,
#         "value": 2.0
#     },
#     "lastValue": {
#         "timestamp": 1621508400000,
#         "value": 6.5
#     },
#     "parameters": {
#         "service": {
#             "id": "1",
#             "label": "IRCEL - CELINE: timeseries-api (SOS 2.0)"
#         },
#         "offering": {
#             "id": "6522",
#             "label": "6522 - btx, o-xyleen - procedure"
#         },
#         "feature": {
#             "id": "1112",
#             "label": "41B006 - Bruxelles (Parlement UE)"
#         },
#         "procedure": {
#             "id": "6522",
#             "label": "6522 - btx, o-xyleen - procedure"
#         },
#         "phenomenon": {
#             "id": "482",
#             "label": "1,2-XYLENE O-XYLENE"
#         },
#         "category": {
#             "id": "482",
#             "label": "1,2-XYLENE O-XYLENE"
#         }
#     }
# },]
def transform_timeseries_list_to_table(timeseries_list):
    columns = [
        "TIMESERIES_ID",
        "CATEGORY_ID",
        "STATION_ID",
        "PROCEDURE_ID",
        "PROCEDURE",
        "UOM",
        "FIRST_VALUE",
        "FIRST_VALUE_TIME",
        "LAST_VALUE",
        "LAST_VALUE_TIME",
    ]
    data = []
    for timeseries_item in timeseries_list:
        data.append(
            [
                timeseries_item["id"],
                timeseries_item["parameters"]["category"]["id"],
                timeseries_item["station"]["properties"]["id"],
                timeseries_item["parameters"]["procedure"]["id"],
                timeseries_item["parameters"]["procedure"]["label"],
                timeseries_item["uom"],
                timeseries_item["firstValue"]["value"],
                dt.fromtimestamp(timeseries_item["firstValue"]["timestamp"] / 1000),
                timeseries_item["lastValue"]["value"],
                dt.fromtimestamp(timeseries_item["lastValue"]["timestamp"] / 1000),
            ]
        )

    return pd.DataFrame(data, columns=columns).convert_dtypes()


# {
# "7066": {
#     "values": [
#         {
#             "timestamp": 1376690400000,
#             "value": 2.0
#         },
#         {
#             "timestamp": 1376694000000,
#             "value": 2.0
#         },
#     ]
# }


def transform_datapoints_to_table(datapoints):
    columns = ["TIMESERIES_ID", "TIME", "VALUE"]
    data = []
    for timeseries_id in datapoints:
        for data_point in datapoints[timeseries_id]["values"]:
            data.append(
                [
                    timeseries_id,
                    dt.fromtimestamp(data_point["timestamp"] / 1000),
                    data_point["value"],
                ]
            )

    return pd.DataFrame(data, columns=columns).convert_dtypes()
