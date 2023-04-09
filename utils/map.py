import streamlit as st
import pydeck as pdk


def show_map(lat, lon, radius_meters, events):
    COLOR_RANGE = [
        [255, 174, 0],
        [255, 138, 25],
        [255, 104, 49],
        [255, 69, 74],
        [255, 35, 100],
    ]

    BREAKS = [20, 40, 60, 80, 100]

    def color_scale(val):
        for i, b in enumerate(BREAKS):
            if val < b:
                return COLOR_RANGE[i]
        return COLOR_RANGE[i]

    geojson_features = []

    for event in events["results"]:
        geojson_features.append(
            {
                "type": "Feature",
                "geometry": event["geo"]["geometry"],
                # NOTE: Not valid GeoJSON, but required for pydeck tooltips (which cannot use properties.* format)
                "title": event["title"],
                "id": event["id"],
                "title": event["title"],
                "phq_attendance": event["phq_attendance"]
                if event["phq_attendance"]
                else "0",
                "phq_attendance_formatted": "{:,}".format(event["phq_attendance"])
                if event["phq_attendance"]
                else "0",
                "phq_rank": event["rank"],
                "local_rank": event["local_rank"],
                "category": event["category"],
                "fill_color": color_scale(
                    event["local_rank"] if event["local_rank"] else 0
                ),
            }
        )

    st.pydeck_chart(
        pdk.Deck(
            tooltip={
                "html": """
                    <p><b>{title}</b></p>
                    Predicted Attendance: {phq_attendance_formatted}<br />
                    PHQ Rank: {phq_rank}<br />
                    Local Rank: {local_rank}<br />
                    Category: {category}
                """,
            },
            initial_view_state=pdk.ViewState(
                latitude=lat,
                longitude=lon,
                zoom=14,
            ),
            layers=[
                # Radius layer
                pdk.Layer(
                    "ScatterplotLayer",
                    data=[{"coordinates": [lon, lat], "radius": radius_meters}],
                    get_position="coordinates",
                    filled=True,
                    get_fill_color="[0, 140, 211, 40]",
                    get_radius="radius",
                ),
                # Center point layer
                pdk.Layer(
                    "IconLayer",
                    data=[
                        {
                            "coordinates": [lon, lat],
                            "radius": radius_meters,
                            "icon_data": {
                                "url": "app/static/restaurant-icon.png",
                                "width": 160,
                                "height": 160,
                            },
                        }
                    ],
                    get_position="coordinates",
                    get_icon="icon_data",
                    get_size=20,
                    pickable=False,
                ),
                # Point-type events layer
                pdk.Layer(
                    "GeoJsonLayer",
                    data=list(
                        filter(
                            lambda x: x["geometry"]["type"] == "Point", geojson_features
                        )
                    ),
                    auto_highlight=True,
                    pickable=True,
                    filled=True,
                    get_fill_color="fill_color",
                    stroked=False,
                    opacity=0.8,
                    get_point_radius=20,
                ),
                # Polygon-type events layer
                pdk.Layer(
                    "GeoJsonLayer",
                    data=list(
                        filter(
                            lambda x: x["geometry"]["type"] != "Point", geojson_features
                        )
                    ),
                    auto_highlight=True,
                    pickable=True,
                    filled=True,
                    stroked=True,
                    get_line_color="fill_color",
                    get_fill_color="fill_color",
                    opacity=0.1,
                    get_line_width=10,
                ),
            ],
        )
    )
