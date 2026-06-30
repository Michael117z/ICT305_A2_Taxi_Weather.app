"""
map.py

Interactive operations map.
"""

import folium

from streamlit_folium import st_folium

import streamlit as st

REGION_COORDS = {

    "Central": (1.290, 103.850),

    "North": (1.430, 103.820),

    "Northeast": (1.380, 103.900),

    "East": (1.340, 103.960),

    "West": (1.340, 103.700),
}

# Representative rainfall station for each operational region
REGIONAL_RAIN_STATIONS = {
    "Woodlands Drive 62": {
        "region": "North",
        "latitude": 1.43944,
        "longitude": 103.80389
    },
    "Compassvale Lane": {
        "region": "North-east",
        "latitude": 1.38666,
        "longitude": 103.89797
    },
    "Tuas South Avenue 3": {
        "region": "West",
        "latitude": 1.2938,
        "longitude": 103.6184
    },
    "Sentosa": {
        "region": "Central",
        "latitude": 1.2504,
        "longitude": 103.8275
    },
    "Changi East Close": {
        "region": "East",
        "latitude": 1.31363,
        "longitude": 104.00317
    }
}

"""
Taxi availability is reported per-region, not per-vehicle, so the map
represents it with circle markers sized/coloured by count rather than
a point-density HeatMap (there are only ~6 distinct coordinates in the
taxi data, one per region).
"""

TAXI_COLOUR_THRESHOLDS = [
    (100, "red"),
    (350, "orange"),
    (float("inf"), "green"),
]

def get_taxi_colour(taxis):
    for threshold, colour in TAXI_COLOUR_THRESHOLDS:
        if taxis < threshold:
            return colour
    return "green"
 
 
def get_taxi_radius(taxis, min_taxis, max_taxis):
    # Scale marker radius between 12px and 40px based on taxi count,
    # so regions with more available taxis show up as visibly larger.
    if max_taxis == min_taxis:
        return 25
 
    scale = (taxis - min_taxis) / (max_taxis - min_taxis)
    return 12 + (scale * 28)

def get_status(taxis, rain):

    if taxis < 100:
        return "Critical", "red"

    elif taxis < 350:
        return "Monitor", "orange"

    elif rain > 4:
        return "Monitor", "orange"

    else:
        return "Healthy", "green"

def show_operations_map(
    taxi_df,
    rainfall_df,
    region_df
):
    st.subheader("🗺️ Operations Map")

    st.info(
    """
    Visualises taxi density, rainfall stations and regional fleet status.

    Operators can quickly identify regions requiring additional taxi deployment without analysing multiple charts individually.
    """
    )

    map_layer = st.radio(
        "Map layer",
        options=[
            "Taxi Density by Region",
            "Rainfall Stations",
            "Regional Status",
        ],
        index=0,
        horizontal=True,
    )
 
    show_taxi_density = map_layer == "Taxi Density by Region"
    show_rain = map_layer == "Rainfall Stations"
    show_regions = map_layer == "Regional Status"

    m = folium.Map(
        location=[1.3521,103.8198],
        zoom_start=11,
        control_scale=True
    )

    if show_taxi_density:
 
        # Average taxi availability per coordinate (region), since the
        # source data only has one point per region rather than per-taxi
        # GPS pings — a HeatMap would just stack identical points.
        density = (
            taxi_df
            .groupby(["region", "latitude", "longitude"])["available_for_hire_taxis"]
            .mean()
            .reset_index()
        )
 
        min_taxis = density["available_for_hire_taxis"].min()
        max_taxis = density["available_for_hire_taxis"].max()
 
        for _, row in density.iterrows():
 
            region = row["region"]
            taxis = row["available_for_hire_taxis"]
            colour = get_taxi_colour(taxis)
            radius = get_taxi_radius(taxis, min_taxis, max_taxis)
 
            folium.CircleMarker(
                location=[
                    row["latitude"],
                    row["longitude"]
                ],
                radius=radius,
                color=colour,
                fill=True,
                fill_color=colour,
                fill_opacity=0.5,
                weight=2,
                tooltip=region,
                popup=folium.Popup(
                    f"<b>{region}</b><br>"
                    f"<b>Average taxis available:</b> {taxis:.0f}",
                    max_width=250
                )
            ).add_to(m)

    if show_rain:

        # Display only one representative rainfall station for each region
        for station_name, station in REGIONAL_RAIN_STATIONS.items():

            # Find this station in the rainfall dataframe
            station_data = rainfall_df[
                rainfall_df["station_name"] == station_name
            ]

            # Skip if this station does not exist in the dataframe
            if station_data.empty:
                continue

            row = station_data.iloc[0]

            # Determine marker colour based on rainfall amount
            if row["rain_mm"] == 0:
                colour = "green"

            elif row["rain_mm"] < 2:
                colour = "lightgreen"

            elif row["rain_mm"] < 4:
                colour = "orange"

            else:
                colour = "red"

            # Add rainfall station marker
            popup_html = f"""
            <b>{station_name}</b><br>
            <b>Region:</b> {station['region']}<br>
            <b>Rainfall:</b> {row['rain_mm']:.1f} mm
            """

            folium.Marker(
                location=[
                    station["latitude"],
                    station["longitude"]
                ],
                popup=folium.Popup(popup_html,max_width=300),
                tooltip=station_name,
                icon=folium.Icon(
                    color=colour,
                    icon="cloud"
                )
            ).add_to(m)
    
    if show_regions:
        summary = (
                region_df
                .groupby("region")
                .agg(

                    avg_taxis=(
                        "available_for_hire_taxis",
                        "mean"
                    ),
                    avg_rain=(
                        "avg_rain_mm",
                        "mean"
                    )
                )
                .reset_index()

            )

        for _, row in summary.iterrows():
            region = row["region"]

            if region not in REGION_COORDS:
                continue

            lat, lon = REGION_COORDS[region]
            status, colour = get_status(
                row["avg_taxis"],
                row["avg_rain"]
            )

            # Formatting the regional status popup to display line breaks better
            popup_html = f"""
            <b>{region}</b><br>
            <b>Status:</b> {status}<br>
            <b>Average taxis:</b> {row['avg_taxis']:.0f}<br>
            <b>Average rainfall:</b> {row['avg_rain']:.2f} mm
            """

            folium.Marker(
                location=[lat, lon],
                popup=folium.Popup(popup_html, max_width=300),
                tooltip=region,
                icon=folium.Icon(
                    color=colour,
                    icon="info-sign"
                )
            ).add_to(m)   

    st_folium(
        m,
        width="stretch",
        height=700,
        returned_objects=[]
    )


    