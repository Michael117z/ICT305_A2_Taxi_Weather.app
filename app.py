"""
ICT305 Taxi Operations Dashboard

Main application entry point.
"""

import streamlit as st

# Imports
from components.header import show_header

from components.sidebar import (
    create_sidebar,
    filter_region_data
)

from utils.loader import (
    load_region_data,
    load_taxi_data,
    load_rainfall_data,
)

from utils.calculations import calculate_dashboard_metrics

from components.overview import (
    show_overview,
    show_recommendation
)

from components.charts import (
    show_taxi_trend,
    show_rainfall_trend,
    show_region_comparison,
    show_rain_vs_taxi,
)

from components.map import show_operations_map

from components.decision_support import (
    show_decision_support
)

from components.footer import show_footer

from utils.preprocessing import (
    preprocess_region_data,
    preprocess_taxi_data,
    preprocess_rainfall_data,
    filter_taxi_data,
    filter_rainfall_data,
)

st.set_page_config(
    page_title="Taxi Operations Dashboard",
    layout="wide"
)

# Load datasets
region_df = load_region_data()
taxi_df = load_taxi_data()
rainfall_df = load_rainfall_data()

# Preprocess datasets
region_df = preprocess_region_data(region_df)

taxi_df = preprocess_taxi_data(taxi_df)

rainfall_df = preprocess_rainfall_data(
    rainfall_df
)

# Create sidebar
filters = create_sidebar(region_df)

# Apply filters
filtered_region_df = filter_region_data(
    region_df,
    filters
)

filtered_taxi_df = filter_taxi_data(
    taxi_df,
    filters
)

filtered_rain_df = filter_rainfall_data(
    rainfall_df,
    filters
)

if filtered_region_df.empty:

    st.warning(
        "No data matches the selected filters."
    )

    st.stop()

# Show the title headers
show_header(filters)

# Calculate dashboard KPIs
metrics = calculate_dashboard_metrics(
    filtered_region_df
)

# Show KPI cards
show_overview(metrics)

# Recommendation
show_recommendation(metrics)

st.divider()

# 4 Charts
col1, col2 = st.columns(2)

with col1:
    show_taxi_trend(filtered_region_df)

with col2:
    show_rainfall_trend(filtered_region_df)

st.divider()

col3, col4 = st.columns(2)

with col3:
    show_region_comparison(filtered_region_df)

with col4:
    show_rain_vs_taxi(filtered_region_df)

st.divider()

# Interactive map
show_operations_map(
    filtered_taxi_df,
    filtered_rain_df,
    filtered_region_df
)

st.divider()

# Show recommended actions to stakeholders
show_decision_support(
    filtered_region_df,
    metrics
)

show_footer()