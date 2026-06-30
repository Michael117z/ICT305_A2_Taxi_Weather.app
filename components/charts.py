"""
charts.py

Interactive dashboard charts.
"""

import plotly.express as px
import streamlit as st

# -------------------------------
# Chart 1 - Taxi Availability Trend
# This answers: How has taxi availability changed over time?
# -------------------------------
def show_taxi_trend(region_df):

    st.subheader("🚖 Taxi Availability Trend")

    st.caption(
    """
    Shows how taxi availability changes throughout the selected period.

    Taxi operators can identify peak and off-peak operating hours and determine when additional drivers or vehicles may be required.
    """
    )

    hourly = (
        region_df
        .groupby("collection_time")[
            "available_for_hire_taxis"
        ]
        .mean()
        .reset_index()
    )

    fig = px.line(
        hourly,
        x="collection_time",
        y="available_for_hire_taxis",
        markers=True,
        title="Average Available Taxis Over Time"
    )

    fig.update_layout(
        xaxis_title="Time",
        yaxis_title="Available Taxis"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

# -------------------------------
# Chart 2 - Rainfall Trend
# -------------------------------
def show_rainfall_trend(region_df):

    st.subheader("🌧 Rainfall Trend")

    st.caption(
    """
    Shows how rainfall changes over time for the selected filters.

    Operators can identify periods of heavier rainfall that may increase passenger demand and prepare additional taxi supply.
    """
    )

    rainfall = (
        region_df
        .groupby("collection_time")[
            "avg_rain_mm"
        ]
        .mean()
        .reset_index()
    )

    fig = px.line(
        rainfall,
        x="collection_time",
        y="avg_rain_mm",
        markers=True,
        title="Average Rainfall Over Time"
    )

    fig.update_layout(
        xaxis_title="Time",
        yaxis_title="Rainfall (mm)"
    )

    fig.update_yaxes(
        rangemode="tozero"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

# -------------------------------
# Chart 3 - Regional Comparison
# Stakeholders can immediately see which region has more taxis.
# -------------------------------
def show_region_comparison(region_df):

    st.subheader("📍 Regional Taxi Availability")

    st.caption(
    """
    Compares average taxi availability across all selected regions.

    Operators can identify which regions have lower taxi availability and consider redistributing vehicles to improve fleet coverage.
    """
    )

    regional = (
        region_df
        .groupby("region")[
            "available_for_hire_taxis"
        ]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        regional,
        x="region",
        y="available_for_hire_taxis",
        color="available_for_hire_taxis",
        title="Average Taxi Availability by Region"
    )

    fig.update_layout(
        xaxis_title="Region",
        yaxis_title="Average Available Taxis"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

# -------------------------------
# Chart 4 - Scatter plot of rain vs taxi
# Does rainfall appear to coincide with changes in taxi availability?
# -------------------------------
def show_rain_vs_taxi(region_df):
    """
    Scatter plot showing the relationship between
    rainfall and taxi availability.
    """

    st.subheader("🌧🚖 Rainfall vs Taxi Availability")

    st.caption(
    """
    Explores the relationship between regional rainfall and taxi availability.

    If higher rainfall consistently coincides with lower taxi availability, fleet managers can proactively position additional taxis before similar weather conditions occur.
    """
    )

    scatter = (
        region_df
        .groupby("region")
        .agg(
            avg_rain=("avg_rain_mm", "mean"),
            avg_taxis=("available_for_hire_taxis", "mean")
        )
        .reset_index()
    )

    fig = px.scatter(
        scatter,
        x="avg_rain",
        y="avg_taxis",
        color="region",
        size="avg_taxis",
        hover_name="region",
        title="Average Rainfall vs Average Taxi Availability"
    )

    fig.update_layout(
        xaxis_title="Average Rainfall (mm)",
        yaxis_title="Average Available Taxis"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )