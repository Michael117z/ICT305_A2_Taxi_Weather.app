"""
sidebar.py

Creates the global sidebar used throughout the dashboard.
"""

import streamlit as st


def create_sidebar(region_df):
    """
    Create sidebar filters.

    Returns a dictionary containing all selected filters.
    """
    st.sidebar.title("⚙ Dashboard Filters")

    # -------------------------------
    # Date Filter
    # -------------------------------
    dates = sorted(
        region_df["date"].unique()
    )

    selected_dates = st.sidebar.multiselect( # Using multiselect as the dataset only covers one week, date range slider not as useful.
        "Select Date(s)",
        options=dates,
        default=dates
    )

    # -------------------------------
    # Region Filter
    # -------------------------------
    regions = sorted(
        region_df["region"].unique()
    )

    selected_regions = st.sidebar.multiselect(
        "Select Region(s)",
        options=regions,
        default=regions
    )

    # -------------------------------
    # Time Period Filter
    # -------------------------------
    time_periods = [
        "Morning",
        "Afternoon",
        "Evening",
        "Night"
    ]

    selected_periods = st.sidebar.multiselect(
        "Time Period",
        options=time_periods,
        default=time_periods
    )

    # -------------------------------
    # Rain Category
    # -------------------------------
    rain_categories = [
        "No Rain",
        "Light",
        "Moderate",
        "Heavy"
    ]

    selected_rain = st.sidebar.multiselect(
        "Rain Category",
        options=rain_categories,
        default=rain_categories
    )

    # -------------------------------
    # Return filters
    # -------------------------------
    return {

        "dates": selected_dates,

        "regions": selected_regions,

        "time_periods": selected_periods,

        "rain_categories": selected_rain
    }   


# -------------------------------
# Filtering Function
# -------------------------------
def filter_region_data(region_df, filters):
    """
    Apply sidebar selections to the regional dataset.
    """

    filtered_df = region_df.copy()

    filtered_df = filtered_df[
        filtered_df["date"].isin(filters["dates"])
    ]

    filtered_df = filtered_df[
        filtered_df["region"].isin(filters["regions"])
    ]

    filtered_df = filtered_df[
        filtered_df["time_period"].isin(filters["time_periods"])
    ]

    filtered_df = filtered_df[
        filtered_df["rain_category"].isin(filters["rain_categories"])
    ]

    return filtered_df

