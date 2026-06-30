"""
overview.py

Displays Executive Overview KPI cards.
"""

import streamlit as st


def show_overview(metrics):
    """
    Display dashboard KPIs.
    """

    st.subheader("📊 Executive Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "🚖 Avg Available Taxis",
            f"{metrics['avg_taxis']:,}"
        )

    with col2:

        st.metric(
            "🌧 Average Rainfall (mm)",
            metrics["avg_rain"]
        )

    with col3:

        st.metric(
            "📍 Lowest Availability",
            metrics["lowest_region"]
        )

    with col4:

        st.metric(
            "🏆 Highest Availability",
            metrics["highest_region"]
        )

def show_recommendation(metrics):
    """
    Display a simple operational recommendation.
    """

    st.subheader("💡 Operational Recommendation")

    if metrics["avg_rain"] > 4:

        st.warning(
            "Heavy rainfall detected. Monitor taxi availability closely."
        )

    elif metrics["avg_taxis"] < 350:

        st.warning(
            "Taxi availability is below the weekly average. Consider increasing fleet allocation."
        )

    else:

        st.success(
            "Fleet availability appears healthy. No immediate redistribution required."
        )