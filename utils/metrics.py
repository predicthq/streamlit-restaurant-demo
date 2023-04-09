import streamlit as st
import datetime
import pandas as pd
from utils.predicthq import (
    fetch_features,
    fetch_demand_surges,
    fetch_event_counts,
    calc_sum_of_features,
    calc_sum_of_event_counts,
    ATTENDED_CATEGORIES,
    NON_ATTENDED_CATEGORIES,
    PHQ_ATTENDANCE_FEATURES,
)
from utils.map import show_map


def show_metrics():
    location = st.session_state.location if "location" in st.session_state else None
    daterange = st.session_state.daterange if "daterange" in st.session_state else None
    suggested_radius = (
        st.session_state.suggested_radius
        if "suggested_radius" in st.session_state
        else None
    )
    radius = st.session_state.radius if "radius" in st.session_state else None

    if (
        location is not None
        and daterange is not None
        and suggested_radius is not None
        and radius is not None
    ):

        # Pull out date range to make them easier to work with
        date_from = daterange["date_from"]
        date_to = daterange["date_to"]

        # Work out previous date range for delta comparisons
        previous_date_from = date_from - (date_to - date_from)
        previous_date_to = date_from

        # Fetch sum of Predicted Attendance
        phq_attendance_features = fetch_features(
            location["lat"],
            location["lon"],
            radius,
            date_from=date_from,
            date_to=date_to,
            features=PHQ_ATTENDANCE_FEATURES,
        )
        phq_attendance_sum = calc_sum_of_features(
            phq_attendance_features, PHQ_ATTENDANCE_FEATURES
        )

        # Fetch previous predicted attendance
        previous_phq_attendance_features = fetch_features(
            location["lat"],
            location["lon"],
            radius,
            date_from=previous_date_from,
            date_to=previous_date_to,
            features=PHQ_ATTENDANCE_FEATURES,
        )
        previous_phq_attendance_sum = calc_sum_of_features(
            previous_phq_attendance_features, PHQ_ATTENDANCE_FEATURES
        )

        # Work out average daily predicted attendance
        days = (date_to - date_from).days
        average_daily_attendance = phq_attendance_sum / days
        previous_average_daily_attendance = previous_phq_attendance_sum / days

        # Fetch event counts/stats
        counts = fetch_event_counts(
            location["lat"],
            location["lon"],
            radius,
            date_from=date_from,
            date_to=date_to,
            tz=location["tz"],
        )
        attended_events_sum = calc_sum_of_event_counts(counts, ATTENDED_CATEGORIES)
        non_attended_events_sum = calc_sum_of_event_counts(
            counts, NON_ATTENDED_CATEGORIES
        )

        # Fetch event counts/stats for previous period
        previous_counts = fetch_event_counts(
            location["lat"],
            location["lon"],
            radius,
            date_from=previous_date_from,
            date_to=previous_date_to,
            tz=location["tz"],
        )
        previous_attended_events_sum = calc_sum_of_event_counts(
            previous_counts, ATTENDED_CATEGORIES
        )
        previous_non_attended_events_sum = calc_sum_of_event_counts(
            previous_counts, NON_ATTENDED_CATEGORIES
        )

        # Fetch Demand Surges
        demand_surges = fetch_demand_surges(
            location["lat"],
            location["lon"],
            radius,
            date_from=date_from,
            date_to=date_to,
        )
        demand_surges_count = len(demand_surges)

        previous_demand_surges = fetch_demand_surges(
            location["lat"],
            location["lon"],
            radius,
            date_from=previous_date_from,
            date_to=previous_date_to,
        )
        previous_demand_surges_count = len(previous_demand_surges)

        # Display metrics
        col1, col2, col3, col4, col5, col6 = st.columns(6)

        with col1:
            st.metric(
                label="Suggested Radius",
                value=f"{suggested_radius['radius']}{suggested_radius['radius_unit']}",
                help="[Suggested Radius Docs](https://docs.predicthq.com/resources/suggested-radius)",
            )

        with col2:
            delta_pct = calc_delta_pct(phq_attendance_sum, previous_phq_attendance_sum)
            st.metric(
                label="Predicted Attendance",
                value=f"{phq_attendance_sum:,.0f}",
                delta=f"{delta_pct:,.0f}%",
                help=f"The predicted number of people attending events in the selected date range. Previous period: {previous_phq_attendance_sum:,.0f}.",
            )

        with col3:
            delta_pct = calc_delta_pct(
                average_daily_attendance, previous_average_daily_attendance
            )
            st.metric(
                label="Avg Daily Attendance",
                value=f"{average_daily_attendance:,.0f}",
                delta=f"{delta_pct:,.0f}%",
                help=f"The average daily predicted number of people attending events in the selected date range. Previous period: {previous_average_daily_attendance:,.0f}.",
            )

        with col4:
            delta_pct = calc_delta_pct(
                attended_events_sum, previous_attended_events_sum
            )
            st.metric(
                label="Attended Events",
                value=attended_events_sum,
                delta=f"{delta_pct:,.0f}%",
                help=f"Total number of attended events in the selected date range. Previous period: {previous_attended_events_sum}.",
            )

        with col5:
            delta_pct = calc_delta_pct(
                non_attended_events_sum, previous_non_attended_events_sum
            )
            st.metric(
                label="Non-Attended Events",
                value=non_attended_events_sum,
                delta=f"{delta_pct:,.0f}%",
                help=f"Total number of non-attended events in the selected date range. Previous period: {previous_non_attended_events_sum}.",
            )

        with col6:
            delta_pct = calc_delta_pct(
                demand_surges_count, previous_demand_surges_count
            )
            st.metric(
                label="Demand Surges",
                value=demand_surges_count,
                delta=f"{delta_pct:,.0f}%",
                help=f"Number of [Demand Surges](https://docs.predicthq.com/resources/demand-surge) in the selected date range. Previous period: {previous_demand_surges_count}.",
            )


def calc_delta_pct(current, previous):
    return ((current - previous) / previous * 100) if previous > 0 else 0
