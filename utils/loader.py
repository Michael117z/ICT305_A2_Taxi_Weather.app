"""
loader.py

Loads all CSV datasets used by the dashboard.
"""

import pandas as pd
import streamlit as st

# Using cache_data as without it, Streamlit re-executes the entire script 
# from top to bottom every time a user interacts with the app 
# (e.g., clicking a button or sorting a table), which forces the CSV to reload 
# from the disk repeatedly

@st.cache_data
def load_region_data():
    """
    Load the regional summary dataset.
    """

    df = pd.read_csv(
        "data/region_live_log.csv"
    )

    return df

@st.cache_data
def load_taxi_data():
    """
    Load taxi GPS dataset.
    """

    df = pd.read_csv(
        "data/taxi_live_log.csv"
    )

    return df

@st.cache_data
def load_rainfall_data():
    """
    Load rainfall station dataset.
    """

    df = pd.read_csv(
        "data/rainfall_live_log.csv"
    )

    return df