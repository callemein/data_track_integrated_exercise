import awswrangler as wr

import streamlit as st
import pandas as pd
import folium

s3_bucket = "data-track-integrated-exercise"
s3_prefix = "timothy-data"
s3_stations_table = "stations.csv"


# Function to create a Folium map
def create_map(df):
    st.subheader("Map of Stations")
    
    # Create a Folium map centered around the mean of latitude and longitude
    map_center = [df['LATITUDE'].mean(), df['LONGITUDE'].mean()]
    my_map = folium.Map(location=map_center, zoom_start=12)

    # Add markers for each data point
    for index, row in df.iterrows():
        folium.Marker(
            location=[row['LATITUDE'], row['LONGITUDE']],
            popup=row['STATION_NAME'],  # You can customize the popup content
            icon=folium.Icon(color='blue')
        ).add_to(my_map)

    # Display the map
    st.markdown(my_map._repr_html_(), unsafe_allow_html=True)

# Streamlit app
def main():

    df = wr.s3.read_csv(f"s3://{s3_bucket}/{s3_prefix}/{s3_stations_table}")

    st.title("Stations Map")

    # Create and display the map
    st.map(df)


    # Display the first few rows of the DataFrame
    st.write("Data Preview:")
    st.dataframe(df.head())

# Run the Streamlit app
if __name__ == "__main__":
    main()