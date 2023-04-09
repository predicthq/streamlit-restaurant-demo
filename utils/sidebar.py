import streamlit as st
import datetime
from utils.predicthq import get_api_key, get_predicthq_client
from utils.code_examples import get_code_example


def show_sidebar_options():
    locations = [
        {
            "id": "san-francisco",
            "name": "San Francisco, US",
            "address": "30 Fremont St",
            "lat": 37.79075,
            "lon": -122.39754,
            "tz": "America/Los_Angeles",
            "units": "imperial",
        },
        {
            "id": "new-york",
            "name": "New York, US",
            "address": "121 Reade St",
            "lat": 40.71714,
            "lon": -74.00969,
            "tz": "America/New_York",
            "units": "imperial",
        },
        {
            "id": "los-angeles",
            "name": "Los Angeles, US",
            "address": "816 S Figueroa St",
            "lat": 34.04977,
            "lon": -118.26218,
            "tz": "America/Los_Angeles",
            "units": "imperial",
        },
        {
            "id": "toronto",
            "name": "Toronto, CA",
            "address": "200 King Street West",
            "lat": 43.64812,
            "lon": -79.38559,
            "tz": "America/Toronto",
            "units": "metric",
        },
        {
            "id": "london",
            "name": "London, UK",
            "address": "Parker Mews",
            "lat": 51.51612,
            "lon": -0.12266,
            "tz": "Europe/London",
            "units": "metric",
        },
        {
            "id": "paris",
            "name": "Paris, FR",
            "address": "14 Rue Croix des Petits Champs",
            "lat": 48.86409,
            "lon": 2.33944,
            "tz": "Europe/Paris",
            "units": "metric",
        },
        {
            "id": "berlin",
            "name": "Berlin, DE",
            "address": "Leipziger Pl. 12",
            "lat": 52.51231,
            "lon": 13.38184,
            "tz": "Europe/Berlin",
            "units": "metric",
        },
        {
            "id": "sydney",
            "name": "Sydney, AU",
            "address": "Lang St",
            "lat": -33.86333,
            "lon": 151.20590,
            "tz": "Australia/Sydney",
            "units": "metric",
        },
        {
            "id": "auckland",
            "name": "Auckland, NZ",
            "address": "31 Customs Street West",
            "lat": -36.84316,
            "lon": 174.76427,
            "tz": "Pacific/Auckland",
            "units": "metric",
        },
    ]

    # Work out which location is currently selected
    index = 0

    if "location" in st.session_state:
        for idx, location in enumerate(locations):
            if st.session_state["location"]["id"] == location["id"]:
                index = idx
                break

    location = st.sidebar.selectbox(
        "Restaurant",
        locations,
        index=index,
        format_func=lambda x: x["name"],
        help="Select the restaurant location.",
        disabled=get_api_key() is None,
        key="location",
    )

    # Prepare the date range (today + 30d as the default)
    today = datetime.date.today()
    date_options = [
        {
            "name": "Next 7 days",
            "date_from": today,
            "date_to": today + datetime.timedelta(days=7),
        },
        {
            "name": "Next 30 days",
            "date_from": today,
            "date_to": today + datetime.timedelta(days=30),
        },
        {
            "name": "Next 90 days",
            "date_from": today,
            "date_to": today + datetime.timedelta(days=90),
        },
    ]

    index = (
        date_options.index(st.session_state.daterange)
        if "daterange" in st.session_state
        else 0
    )
    st.sidebar.selectbox(
        "Date Range",
        date_options,
        index=index,
        format_func=lambda x: x["name"],
        help="Select the date range for fetching event data.",
        disabled=get_api_key() is None,
        key="daterange",
    )

    # Use an appropriate radius unit depending on location
    radius_unit = (
        "mi" if "units" in location and location["units"] == "imperial" else "km"
    )

    st.session_state.suggested_radius = fetch_suggested_radius(
        location["lat"], location["lon"], radius_unit=radius_unit
    )

    # Allow changing the radius if needed (default to suggested radius)
    # The Suggested Radius API is used to determine the best radius to use for the given location and industry
    st.sidebar.slider(
        f"Suggested Radius around restaurant ({radius_unit})",
        0.0,
        10.0,
        st.session_state.suggested_radius.get("radius", 2.0),
        0.1,
        help="[Suggested Radius Docs](https://docs.predicthq.com/resources/suggested-radius)",
        key="radius",
    )


@st.cache_data
def fetch_suggested_radius(lat, lon, radius_unit="mi", industry="restaurants"):
    phq = get_predicthq_client()
    suggested_radius = phq.radius.search(
        location__origin=f"{lat},{lon}", radius_unit=radius_unit, industry=industry
    )

    return suggested_radius.to_dict()


def show_map_sidebar_code_examples():
    st.sidebar.markdown("## Code examples")

    # The code examples are saved as markdown files in docs/code_examples
    examples = [
        {"name": "Suggested Radius API", "filename": "suggested_radius_api"},
        {
            "name": "Features API (Predicted Attendance aggregation)",
            "filename": "features_api",
        },
        {"name": "Count of Events", "filename": "count_api"},
        {"name": "Demand Surge API", "filename": "demand_surge_api"},
        {"name": "Search Events", "filename": "events_api"},
        {"name": "Python SDK for PredictHQ APIs", "filename": "python_sdk"},
    ]

    for example in examples:
        with st.sidebar.expander(example["name"]):
            st.markdown(get_code_example(example["filename"]))

    st.sidebar.caption(
        "Get the code for this app at [GitHub](https://github.com/predicthq/streamlit-restaurant-demo)"
    )
