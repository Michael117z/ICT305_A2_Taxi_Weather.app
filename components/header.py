"""
Dashboard header.
"""

import streamlit as st


def show_header(filters):

    st.title("🚖 Singapore Taxi Operations Dashboard")

    st.caption(
        "Interactive decision-support dashboard for taxi fleet operators."
    )

    st.info(
    """
    This dashboard analyses historical taxi availability and rainfall data collected over one week.
    Use the filters on the left to explore different operational scenarios.
    """
        )

    st.divider()