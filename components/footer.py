import streamlit as st


def show_footer():

    st.divider()

    st.caption(
        """
        ICT305 Assignment 2 Group Project - Team Wizards

        Dashboard developed using Streamlit in Python code.

        Data Source:
        data.gov.sg Taxi Availability API
        and Rainfall API.
        """
    )