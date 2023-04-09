import streamlit as st
import plotly.express as px
import pandas as pd
from utils.pages import set_page_config
from utils.sidebar import show_sidebar_options
from utils.metrics import show_metrics
from utils.predicthq import (
    get_api_key,
    fetch_features,
    fetch_demand_surges,
    PHQ_ATTENDANCE_FEATURES,
)


def main():
    set_page_config("Demand Surge")
    show_sidebar_options()

    if get_api_key() is not None:
        demand_surge()
    else:
        st.warning(
            "Please set a [PredictHQ API Token](https://docs.predicthq.com/oauth2/introduction).",
            icon="⚠️",
        )


def demand_surge():
    location = st.session_state.location if "location" in st.session_state else None
    daterange = st.session_state.daterange if "daterange" in st.session_state else None
    suggested_radius = (
        st.session_state.suggested_radius
        if "suggested_radius" in st.session_state
        else None
    )
    radius = st.session_state.radius if "radius" in st.session_state else None

    if (
        location is None
        or daterange is None
        or suggested_radius is None
        or radius is None
    ):
        return

    st.header(location["name"])

    # Display metrics
    show_metrics()

    # Pull out date range to make them easier to work with
    date_from = daterange["date_from"]
    date_to = daterange["date_to"]

    # Fetch sum of Predicted Attendance
    phq_attendance_features = fetch_features(
        location["lat"],
        location["lon"],
        radius,
        date_from=date_from,
        date_to=date_to,
        features=PHQ_ATTENDANCE_FEATURES,
    )

    phq_attendance_daily_sum = calc_daily_sum_of_features(
        phq_attendance_features, PHQ_ATTENDANCE_FEATURES
    )

    # Fetch Demand Surges
    demand_surges = fetch_demand_surges(
        location["lat"], location["lon"], radius, date_from=date_from, date_to=date_to
    )

    # Display charts in tabs
    tab1, tab2 = st.tabs(["Total Daily Attendance", "Daily Attendance by Feature"])

    with tab1:
        phq_attendance_daily_sum_df = pd.DataFrame(phq_attendance_daily_sum)

        fig = px.area(
            phq_attendance_daily_sum_df,
            x="date",
            y="phq_attendance_sum",
        )

        for demand_surge in demand_surges:
            fig.add_vline(
                x=demand_surge["date"],
                line_width=5,
                line_color="green",
                opacity=0.5,
                layer="below",
            )

        st.plotly_chart(fig, use_container_width=True, theme="streamlit")
    with tab2:
        features_daily_sum = get_daily_sums_of_features(
            phq_attendance_features, PHQ_ATTENDANCE_FEATURES
        )
        features_daily_sum_df = pd.DataFrame(features_daily_sum)

        fig = px.bar(
            features_daily_sum_df,
            x="date",
            y="phq_attendance_sum",
            color="feature",
        )

        # Add demand surges to the chart
        for demand_surge in demand_surges:
            fig.add_vline(
                x=demand_surge["date"],
                line_width=5,
                line_color="green",
                opacity=0.5,
                layer="below",
            )

        # fig.update_layout(
        #     legend=dict(orientation="h", yanchor="top", y=-0.3, xanchor="right", x=1)
        # )
        fig.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))
        fig.update_layout(legend_title_text="")

        st.plotly_chart(fig, use_container_width=True, theme="streamlit")


def calc_daily_sum_of_features(features_result, features):
    # sum up the attendance features per date
    results = []

    for item in features_result["results"]:
        phq_attendance_sum = 0

        for k, v in item.items():
            phq_attendance_sum += v["stats"]["sum"] if k in features else 0

        results.append(
            {
                "date": item["date"],
                "phq_attendance_sum": phq_attendance_sum,
            }
        )

    return results


def get_daily_sums_of_features(features_result, features):
    # Pull out just the sum of each feature per date
    results = []

    for item in features_result["results"]:

        for k, v in item.items():
            if k in features:
                results.append(
                    {
                        "date": item["date"],
                        "feature": k,
                        "phq_attendance_sum": v["stats"]["sum"],
                    }
                )

    return results


if __name__ == "__main__":
    main()
