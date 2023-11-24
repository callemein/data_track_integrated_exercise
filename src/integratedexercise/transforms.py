# transform functions


def replace_ids_with_reference(timeseries_ids, timeseries):
    transformed_timeseries = {}
    for timeseries_id in timeseries:
        transformed_timeseries[timeseries_ids[timeseries_id]] = timeseries[
            timeseries_id
        ]

    return transformed_timeseries


def transform_stations(stations):
    transformed_stations = {}
    for station in stations:
        id = station["properties"]["id"]
        label = station["properties"]["label"]
        coordinates = station["geometry"]["coordinates"]

        transformed_stations[label] = {
            "id": id,
            "label": label,
            "coordinates": coordinates,
        }

    return transformed_stations
