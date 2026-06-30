"""
preprocessing.py

Creates additional features
used throughout the dashboard.
"""

import pandas as pd


def preprocess_region_data(df):
    """
    Add useful calculated columns to the regional dataset.
    """

    # Convert collection time to datetime
    df["collection_time"] = pd.to_datetime(df["collection_time"])

    # Extract date information
    df["date"] = df["collection_time"].dt.date
    df["hour"] = df["collection_time"].dt.hour
    df["day"] = df["collection_time"].dt.day_name()

    # Weekend flag
    df["is_weekend"] = df["day"].isin(
        ["Saturday", "Sunday"]
    )

    # Get time period
    df["time_period"] = df["hour"].apply(get_time_period)

    # -------------------------------
    # Rain Category
    # Values were referenced from NEA Weather: https://neaweather.com/rain
    # -------------------------------

    def rain_category(rain):

        if rain == 0:
            return "No Rain"

        elif rain < 2:
            return "Light"

        elif rain < 4:
            return "Moderate"

        else:
            return "Heavy"

    df["rain_category"] = df["avg_rain_mm"].apply(
        rain_category
    )

    # -------------------------------
    # Taxi Availability Category
    # -------------------------------

    def taxi_level(taxis):

        if taxis < 100:
            return "Low"

        elif taxis < 350:
            return "Medium"

        else:
            return "High"

    df["availability_level"] = (
        df["available_for_hire_taxis"]
        .apply(taxi_level)
    )

    # Sort by time
    df = df.sort_values("collection_time")

    # Reset index
    df = df.reset_index(drop=True)

    return df

# -------------------------------------------------
# Shared helper
# -------------------------------------------------

def get_time_period(hour):

    if hour < 6:
        return "Night"

    elif hour < 12:
        return "Morning"

    elif hour < 18:
        return "Afternoon"

    else:
        return "Evening"


# -------------------------------------------------
# Taxi preprocessing
# -------------------------------------------------

def preprocess_taxi_data(df):

    df["collection_time"] = pd.to_datetime(
        df["collection_time"]
    )

    df["date"] = df["collection_time"].dt.date

    df["hour"] = df["collection_time"].dt.hour

    df["time_period"] = df["hour"].apply(
        get_time_period
    )

    return df


# -------------------------------------------------
# Rainfall preprocessing
# -------------------------------------------------

def preprocess_rainfall_data(df):

    df["collection_time"] = pd.to_datetime(
        df["collection_time"]
    )

    df["date"] = df["collection_time"].dt.date

    df["hour"] = df["collection_time"].dt.hour

    df["time_period"] = df["hour"].apply(
        get_time_period
    )

    return df


# -------------------------------------------------
# Taxi filtering
# -------------------------------------------------

def filter_taxi_data(df, filters):

    df = df[
        df["date"].isin(filters["dates"])
    ]

    df = df[
        df["time_period"].isin(
            filters["time_periods"]
        )
    ]

    return df


# -------------------------------------------------
# Rainfall filtering
# -------------------------------------------------

def filter_rainfall_data(df, filters):

    df = df[
        df["date"].isin(filters["dates"])
    ]

    df = df[
        df["time_period"].isin(
            filters["time_periods"]
        )
    ]

    return df