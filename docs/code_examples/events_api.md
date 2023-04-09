## Events API

The Events API gives you a read-only interface to PredictHQ's underlying event data. An event represents something happening at a specific date, time and location, which is either scheduled or unscheduled.

```python
import requests

response = requests.get(
    url="https://api.predicthq.com/v1/events/",
    headers={
      "Authorization": "Bearer $ACCESS_TOKEN",
      "Accept": "application/json"
    },
    params={
        "within": "30mi@41.75038,-71.49978",
        "active.gte": "2023-03-30",
        "active.lte": "2023-04-29",
        "active.tz": "America/New_York",
        "category": "concerts,conferences,sports",
        "limit": 20,
        "offset": 0,
        "sort": "rank",
        "state": "active,predicted",
    }
)

print(response.json())
```

Example response:

```json
{
  "count": 154,
  "overflow": false,
  "next": "https://api.predicthq.com/v1/events/?active.gte=2023-03-30&active.lte=2023-04-29&active.tz=Pacific%2FAuckland&category=concerts%2Cconferences%2Csports&limit=20&offset=20&sort=rank&state=active%2Cpredicted&t=1680137347407&within=30mi%4041.75038%2C-71.49978",
  "previous": null,
  "results": [
    {
      "relevance": null,
      "id": "5VPihaao3Zum2WaAza",
      "title": "MLS - New England vs New York City",
      "description": "",
      "category": "sports",
      "labels": [
        "mls",
        "soccer",
        "sport"
      ],
      "rank": 74,
      "local_rank": 100,
      "aviation_rank": 71,
      "phq_attendance": 15776,
      "entities": [
        {
          "entity_id": "w8eDP8Cn2WZZurG6aGE8J6",
          "name": "New England Revolution",
          "type": "organization"
        },
        {
          "entity_id": "zCGFvXDGWtrUAh3WXus3i6",
          "name": "New York City FC",
          "type": "organization"
        },
        {
          "entity_id": "mffNyuzhUxpgv9RaCbVbYK",
          "name": "Gillette Stadium",
          "type": "venue",
          "formatted_address": "1 Patriot Place\nFoxborough, MA 02035\nUnited States of America"
        }
      ],
      "duration": 0,
      "start": "2023-04-01T23:30:00Z",
      "end": "2023-04-01T23:30:00Z",
      "predicted_end": "2023-04-02T01:20:00Z",
      "updated": "2023-03-30T00:05:55Z",
      "first_seen": "2022-12-20T23:39:35Z",
      "timezone": "America/New_York",
      "location": [
        -71.2643465,
        42.0909458
      ],
      "geo": {
        "geometry": {
          "coordinates": [
            -71.2643465,
            42.0909458
          ],
          "type": "Point"
        },
        "placekey": "226-222@62k-nzs-nh5"
      },
      "scope": "locality",
      "country": "US",
      "place_hierarchies": [
        [
          "6295630",
          "6255149",
          "6252001",
          "6254926",
          "4945455",
          "4951631"
        ],
        [
          "6295630",
          "6255149",
          "6252001",
          "6254926",
          "4945455",
          "4934664"
        ]
      ],
      "state": "active",
      "private": false
    },
    ...
  ]
}
```

Full docs for the Events API are available at [https://docs.predicthq.com/resources/events](https://docs.predicthq.com/resources/events)
