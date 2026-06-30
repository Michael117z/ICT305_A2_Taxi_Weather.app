"""
calculations.py

Contains reusable KPI calculations.
"""

import pandas as pd


def calculate_dashboard_metrics(region_df):
    """
    Calculate KPI values for the Executive Overview.
    """

    metrics = {}

    if region_df.empty:

        return {
            "avg_taxis": 0,
            "avg_rain": 0,
            "total_records": 0,
            "regions": 0
        }

    # Average available taxis
    metrics["avg_taxis"] = round(
        region_df["available_for_hire_taxis"].mean()
    )

    # Average rainfall
    metrics["avg_rain"] = round(
        region_df["avg_rain_mm"].mean(),
        2
    )

    # Region with lowest taxi availability
    lowest = region_df.loc[
        region_df["available_for_hire_taxis"].idxmin()
    ]

    metrics["lowest_region"] = lowest["region"]

    # Region with highest taxi availability
    highest = region_df.loc[
        region_df["available_for_hire_taxis"].idxmax()
    ]

    metrics["highest_region"] = highest["region"]

    return metrics