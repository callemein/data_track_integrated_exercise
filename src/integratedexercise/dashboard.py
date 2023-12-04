import awswrangler as wr

import streamlit as st
import pandas as pd
from geopy.geocoders import Nominatim

from geopy.extra.rate_limiter import RateLimiter


s3_bucket = "data-track-integrated-exercise"
s3_prefix = "timothy-data"
s3_stations_table = "stations.csv"

# Streamlit app
def main():

    df = wr.s3.read_csv(f"s3://{s3_bucket}/{s3_prefix}/{s3_stations_table}")

    st.title("Stations")

    # Create and display the map
    st.map(df)

    st.title("City Information")

    # Display the DataFrame with the new 'City' column
    df_counts = df.groupby('CITY')['CITY'].count().reset_index(name='Count')
    st.dataframe(df_counts, use_container_width=True, hide_index=True)


# Run the Streamlit app
if __name__ == "__main__":
    main()