## Demand Surge API

The Demand Surge API can be used to quickly scan a period of 90 days for abnormal increases in attendance for a given area. The API calculates the mean attendance for your requested location across 90 days, then returns all the dates where attendance is a certain number of standard deviations over the mean. This is represented by the min_surge_intensity parameter, which corresponds to the number of standard deviations the API will look for.

Once identified, demand surges can be further explored in our Events or Features APIs, to find the names, descriptions and details of the events that constitute the surges.

```python
import requests

response = requests.get(
    url="https://api.predicthq.com/v1/demand-surge/",
    headers={
      "Authorization": "Bearer $ACCESS_TOKEN",
      "Accept": "application/json"
    },
    params={
        "date_from": "2021-05-12",
        "date_to": "2021-08-10",
        "min_surge_intensity": "m",
        "location.place_id": "2643743"
    }
)

print(response.json())
```

Example response:

```json
{
    "count": 2,
    "surge_dates": [
        {
            "date": "2021-08-07",
            "phq_attendance_sum": 233930
        },
        {
            "date": "2021-08-08",
            "phq_attendance_sum": 213382
        }
    ]
}
```

Full docs for the Demand Surge API are available at [https://docs.predicthq.com/resources/demand-surge](https://docs.predicthq.com/resources/demand-surge)
