## Python SDK

Most of the code examples here are using the Python `requests` library to demonstrate how the APIs work. We also have an SDK available that makes it easier to use the APIs in Python. The SDK is available on [PyPI](https://pypi.org/project/predicthq/) and the code is available on GitHub at [https://github.com/predicthq/sdk-py](https://github.com/predicthq/sdk-py).

Below is an example using the SDK to get the attendance and other stats around a location:

```python
from predicthq import Client

phq = Client(access_token="$ACCESS_TOKEN")

for feature in phq.features.obtain_features(
        active__gte="2017-12-31",
        active__lte="2018-01-02",
        location__geo={
            "lon": -97.74306,
            "lat": 30.26715,
            "radius": "150km"
        },
        phq_rank_public_holidays=True,
        phq_attendance_sports__stats=["count", "median"],
        phq_attendance_sports__phq_rank={
            "gt": 50
        }
):
    print(feature.date, feature.phq_attendance_sports.stats.count, feature.phq_rank_public_holidays.rank_levels)

```

Here's an example using the SDK to get the suggested radius for a location:

```python
from predicthq import Client

phq = Client(access_token="$ACCESS_TOKEN")

suggested_radius = phq.radius.search(location__origin="45.5051,-122.6750")
print(suggested_radius.radius, suggested_radius.radius_unit, suggested_radius.location.to_dict())
```

Docs for the Python SDK are available at [https://docs.predicthq.com/sdks/python](https://docs.predicthq.com/sdks/python)
