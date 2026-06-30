"""
decision_support.py

Provides operational recommendations
for taxi fleet managers based on the
selected dashboard filters.
"""

import streamlit as st


# ------------------------------------------
# Dashboard Thresholds
# ------------------------------------------

CRITICAL_THRESHOLD = 100

MONITOR_THRESHOLD = 350

HEAVY_RAIN_THRESHOLD = 4


# ------------------------------------------
# Decision Support
# ------------------------------------------

def show_decision_support(df, metrics):

    st.header("🚦 Operations Control Centre")

    st.info(
    """
    Summarises operational recommendations based on the selected data.

    Provides fleet deployment suggestions and highlights regions that require immediate attention.
    """
    )

    # ------------------------------------------
    # Stop if no data
    # ------------------------------------------

    if df.empty:

        st.warning(
            "No data available for the selected filters."
        )

        return

    avg_taxis = metrics["avg_taxis"]

    avg_rain = metrics["avg_rain"]

    lowest_region = metrics["lowest_region"]

    highest_region = metrics["highest_region"]

    # ==========================================
    # Top Control Cards
    # ==========================================

    col1, col2, col3 = st.columns(3)

    # ------------------------------------------
    # Fleet Status
    # ------------------------------------------

    with col1:

        st.subheader("🚖 Fleet Status")

        if avg_taxis < CRITICAL_THRESHOLD:

            st.error("🔴 Critical")
            st.write(
                "Immediate deployment of additional taxis is recommended."
            )

        elif avg_taxis < MONITOR_THRESHOLD:

            st.warning("🟠 Monitor")
            st.write(
                "Taxi availability is decreasing. Continue monitoring demand."
            )

        else:

            st.success("🟢 Healthy")
            st.write(
                "Taxi supply is currently sufficient."
            )

    # ------------------------------------------
    # Fleet Deployment
    # ------------------------------------------

    with col2:

        st.subheader("📍 Fleet Deployment")

        st.metric(
            label="Recommended Movement",
            value=f"{highest_region} ➜ {lowest_region}"
        )

        st.caption(
            "Based on average taxi availability."
        )

    # ------------------------------------------
    # Weather Impact
    # ------------------------------------------

    with col3:

        st.subheader("🌧 Weather Impact")

        if avg_rain > HEAVY_RAIN_THRESHOLD:

            st.warning("Higher demand expected")

            st.write(
                """
                Consider deploying more taxis near:

                • MRT stations

                • Shopping malls

                • CBD

                • Bus interchanges
                """
            )

        else:

            st.success("Minimal weather impact")
            st.write(
                "Normal operating conditions."
            )

    st.divider()

    # ==========================================
    # Regional Operations Summary
    # ==========================================

    st.subheader("📋 Regional Operations Summary")

    summary = (

        df.groupby("region")

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
        .round(2)
        .reset_index()

    )

    # ------------------------------------------
    # Regional Status
    # ------------------------------------------

    def get_status(row):

        if row["avg_taxis"] < CRITICAL_THRESHOLD:
            return "🔴 Critical"
        elif row["avg_taxis"] < MONITOR_THRESHOLD:
            return "🟠 Monitor"
        else:
            return "🟢 Healthy"

    # ------------------------------------------
    # Regional Recommended Action
    # ------------------------------------------

    def get_action(row):

        if row["avg_taxis"] < CRITICAL_THRESHOLD:
            return "Deploy additional taxis and postpone driver breaks"
        elif row["avg_taxis"] < MONITOR_THRESHOLD:
            return "Relocate nearby idle taxis to this region"
        elif row["avg_rain"] > HEAVY_RAIN_THRESHOLD:
            return "Prepare extra taxis near MRT stations and malls"
        else:
            return "Maintain current fleet allocation"

    summary["Status"] = summary.apply(
        get_status,
        axis=1

    )

    summary["Recommended Action"] = summary.apply(
        get_action,
        axis=1
    )

    summary = summary[
        [
            "region",
            "avg_taxis",
            "avg_rain",
            "Status",
            "Recommended Action"
        ]
    ]

    st.dataframe(
        summary,
        width="stretch",
        hide_index=True

    )

