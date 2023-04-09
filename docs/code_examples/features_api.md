## Features API

The Features API provides features for ML Models across all types of demand causal factors, including attended events and non-attended events.

It allows you to go straight to feature-importance testing and improving your models rather than having to worry about first building a data lake and then aggregating the data.

```python
import requests

data = {
    "active": {
        "gte": "2019-11-16",
        "lte": "2019-11-27"
    },
    "location": {
        "geo": {
            "lon": -71.49978,
            "lat": 41.75038,
            "radius": "30mi"
        }
    },
    "phq_attendance_conferences": {
        "stats": [
            "min",
            "max"
        ]
    },
    "phq_attendance_sports": {
        "stats": ["count", "std_dev", "median"],
        "phq_rank": { 
            "gt": 50
        }    
    },
    "phq_attendance_concerts": True,
    "phq_rank_public_holidays": True
}


response = requests.post(
    url="https://api.predicthq.com/v1/features",
    headers={
      "Authorization": "Bearer $ACCESS_TOKEN",
      "Accept": "application/json"
    },
    json=data
)

print(response.json())
```

Example response:

```json
{
    "results": [
        {
            "date": "2019-11-16",
            "phq_attendance_concerts": {
                "stats": {
                    "count": 16,
                    "sum": 4972
                }
            },
            "phq_attendance_conferences": {
                "stats": {
                    "count": 1,
                    "min": 1500,
                    "max": 1500
                }
            },
            "phq_attendance_sports": {
                "stats": {
                    "count": 4,
                    "median": 2859.5,
                    "std_dev": 3189.0008231419447
                }
            },
            "phq_rank_public_holidays": {
                "rank_levels": {
                    "1": 0,
                    "2": 0,
                    "3": 0,
                    "4": 0,
                    "5": 0
                }
            }
        },
        {
            "date": "2019-11-17",
            "phq_attendance_concerts": {
                "stats": {
                    "count": 1,
                    "sum": 200
                }
            },
            "phq_attendance_conferences": {
                "stats": {
                    "count": 0,
                    "min": 0,
                    "max": 0
                }
            },
            "phq_attendance_sports": {
                "stats": {
                    "count": 0,
                    "median": 0.0,
                    "std_dev": null
                }
            },
            "phq_rank_public_holidays": {
                "rank_levels": {
                    "1": 0,
                    "2": 0,
                    "3": 0,
                    "4": 0,
                    "5": 0
                }
            }
        }
    ]
}
```

The way the total sum of Predicted Attendance is calculated in this app is by requesting the `phq_attendance_*` features, then looping through the results to sum the numbers together.

Full docs for the Features API are available at [https://docs.predicthq.com/resources/features](https://docs.predicthq.com/resources/features)
