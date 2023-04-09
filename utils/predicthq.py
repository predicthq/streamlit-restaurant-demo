import datetime
import requests
import streamlit as st
from predicthq import Client


ATTENDED_CATEGORIES = [
    "community",
    "concerts",
    "conferences",
    "expos",
    "festivals",
    "performing-arts",
    "sports",
]
NON_ATTENDED_CATEGORIES = [
    "academic",
    "daylight-savings",
    "observances",
    "politics",
    "public-holidays",
    "school-holidays",
]
UNSCHEDULED_CATEGORIES = [
    "airport-delays",
    "disasters",
    "health-warnings",
    "severe-weather",
    "terror",
]

# Some of the possible phq_attendance features are commented out below to match what
# we do in our Location Insights product. You can uncomment them to include them in.
PHQ_ATTENDANCE_FEATURES = [
    # "phq_attendance_academic_graduation",
    # "phq_attendance_academic_social",
    "phq_attendance_community",
    "phq_attendance_concerts",
    "phq_attendance_conferences",
    "phq_attendance_expos",
    "phq_attendance_festivals",
    "phq_attendance_performing_arts",
    "phq_attendance_sports",
    # "phq_attendance_school_holidays",
]


def get_api_key():
    return st.secrets["api_key"]


def get_predicthq_client():
    api_key = get_api_key()
    phq = Client(access_token=api_key)

    return phq


@st.cache_data
def fetch_features(lat, lon, radius, date_from, date_to, features=[], radius_unit="mi"):
    """
    Features API only works with local time, so any date range used is based on the timezone
    at the location being queried.
    """
    phq = get_predicthq_client()
    features = phq.features.obtain_features(
        location__geo={
            "lat": lat,
            "lon": lon,
            "radius": f"{radius}{radius_unit}",
        },
        active={
            "gte": date_from,
            "lte": date_to,
        },
        **{feature: True for feature in features},
    )

    return features.to_dict()


@st.cache_data
def fetch_demand_surges(
    lat, lon, radius, date_from, date_to, min_surge_intensity="m", radius_unit="mi"
):
    """
    The Demand Surge API works with local time just like the Features API.
    """
    r = requests.get(
        url="https://api.predicthq.com/v1/demand-surge",
        headers={
            "Authorization": f"Bearer {get_api_key()}",
            "Accept": "application/json",
        },
        params={
            "location.origin": f"{lat},{lon}",
            "location.radius": f"{radius}{radius_unit}",
            "date_from": date_from,
            "date_to": date_from + datetime.timedelta(days=90),
            "min_surge_intensity": min_surge_intensity,
        },
        allow_redirects=False,
    )

    json = r.json()
    results = []

    for demand_surge in json["surge_dates"]:
        # When fetching demand surge dates from the API we have to use a 90d period,
        # so we need to filter out the dates that are outside of the date range we're interested in.
        date = datetime.datetime.strptime(demand_surge["date"], "%Y-%m-%d").date()

        if date_from <= date <= date_to:
            results.append(demand_surge)

    return results


@st.cache_data
def fetch_events(
    lat, lon, radius, date_from, date_to, tz="UTC", categories=[], radius_unit="mi"
):
    """
    Events API works with UTC time and you can specify a different timezone for the date range
    but all results are always in UTC so must be converted to the local timezone.
    """
    phq = get_predicthq_client()
    events = phq.events.search(
        within=f"{radius}{radius_unit}@{lat},{lon}",
        active={
            "gte": date_from,
            "lte": date_to,
            "tz": tz,
        },
        category=",".join(categories),
        state="active",
        limit=200,
        sort="phq_attendance",
    )

    return events.to_dict()


@st.cache_data
def fetch_event_counts(
    lat, lon, radius, date_from, date_to, tz="UTC", radius_unit="mi"
):
    phq = get_predicthq_client()
    counts = phq.events.count(
        within=f"{radius}{radius_unit}@{lat},{lon}",
        active={
            "gte": date_from,
            "lte": date_to,
            "tz": tz,
        },
        state="active",
    )

    return counts.to_dict()


def calc_sum_of_features(features_result, features):
    # sum up the attendance features
    phq_attendance_sum = 0

    for item in features_result["results"]:
        for k, v in item.items():
            phq_attendance_sum += v["stats"]["sum"] if k in features else 0

    return phq_attendance_sum


def calc_sum_of_event_counts(counts_result, categories):
    counts = {k: v for k, v in counts_result["categories"].items() if k in categories}

    return sum(counts.values())
