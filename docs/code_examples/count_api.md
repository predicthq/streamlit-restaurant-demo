# Count API

This endpoint uses the same parameters as Events API and can be used to get counts of all matching events (that are available to your account).


```python
import requests

response = requests.get(
    url="https://api.predicthq.com/v1/events/count/",
    headers={
      "Authorization": "Bearer $ACCESS_TOKEN",
      "Accept": "application/json"
    },
    params={
        "country": "NZ"
    }
)

print(response.json())
```

Example response:

```json
{
  "count": 271423,
  "top_rank": 100.0,
  "top_local_rank": 100.0,
  "top_aviation_rank": 100.0,
  "rank_levels": {
    "1": 163349,
    "2": 75098,
    "3": 17178,
    "4": 5873,
    "5": 9925
  },
  "local_rank_levels": {
    "1": 10524,
    "2": 143054,
    "3": 76958,
    "4": 16460,
    "5": 6323
  },
  "aviation_rank_levels": {
    "1": 25952,
    "2": 78,
    "3": 987,
    "4": 767,
    "5": 212
  },
  "categories": {
    "academic": 2300,
    "airport-delays": 16570,
    "community": 27100,
    "concerts": 44056,
    "conferences": 72503,
    "daylight-savings": 26,
    "disasters": 418,
    "expos": 1601,
    "festivals": 47931,
    "health-warnings": 28,
    "observances": 198,
    "performing-arts": 52698,
    "politics": 12,
    "public-holidays": 434,
    "school-holidays": 38,
    "severe-weather": 277,
    "sports": 7519,
    "terror": 14
  },
  "labels": {
    "agriculture": 60,
    "airport": 16570,
    "american-football": 10,
    "animal": 12,
    "architecture": 6,
    "arson": 11,
    "attack": 12,
    "attraction": 8904,
    "auto-racing": 7,
    "automotive": 20,
    "avalanche": 2,
    "baseball": 21,
    "basketball": 271,
    "bicycle": 1,
    "blizzard": 1,
    "bombing": 2,
    "boxing": 10,
    "business": 3364,
    "campus": 575,
    "career": 187,
    "chemical": 3,
    "closed-doors": 4,
    "clothing": 26,
    "club": 200,
    "cold-wave": 1,
    "comedy": 914,
    "comic": 15,
    "community": 4616,
    "concert": 70570,
    "conference": 72510,
    "construction": 71,
    "course": 2,
    "craft": 41,
    "cricket": 1064,
    "cyclone": 1,
    "daylight-savings": 26,
    "delay": 16570,
    "design": 6,
    "digital": 36,
    "disaster": 418,
    "drought": 3,
    "earthquake": 298,
    "education": 64667,
    "election": 7,
    "entertainment": 3253,
    "environment": 6,
    "epidemic": 1,
    "epidemic-hazard": 28,
    "expo": 1602,
    "family": 9484,
    "fashion": 165,
    "festival": 48574,
    "fire": 54,
    "flood": 106,
    "food": 824,
    "fundraiser": 2161,
    "furniture": 4,
    "gaming": 4,
    "health": 9829,
    "health-warning": 28,
    "heat-wave": 2,
    "hockey": 10,
    "holiday": 670,
    "holiday-local": 286,
    "holiday-national": 148,
    "household": 401,
    "ice-hockey": 20,
    "industrial": 93,
    "instrument": 19,
    "jewelry": 2,
    "landslide": 6,
    "lockdown": 4,
    "marathon": 210,
    "marine": 1,
    "medical": 222,
    "mineral": 2,
    "movie": 3431,
    "music": 71698,
    "natural": 2,
    "observance": 198,
    "observance-season": 52,
    "outdoor": 8663,
    "packaging": 9,
    "parliament": 7,
    "performing-arts": 55955,
    "pet": 3,
    "politics": 390,
    "print": 1,
    "product": 41,
    "rain": 13,
    "referendum": 5,
    "religion": 3234,
    "research-development": 1,
    "rugby": 1837,
    "running": 348,
    "school": 39,
    "science": 1019,
    "seminar": 4,
    "skating": 2,
    "snow": 3,
    "soccer": 3870,
    "social": 7557,
    "sport": 8159,
    "storm": 37,
    "technology": 1473,
    "tennis": 4,
    "terror": 14,
    "tornado": 42,
    "training": 1,
    "transportation": 51,
    "travel": 26,
    "tsunami": 10,
    "volcano": 28,
    "volleyball": 1,
    "weather": 277,
    "weather-warning": 6,
    "wedding": 1,
    "wildfire": 35,
    "wind": 9,
    "wrestling": 3
  }
}
```


Full docs for the Count API are available at [https://docs.predicthq.com/resources/events/#retrieve-events-count](https://docs.predicthq.com/resources/events/#retrieve-events-count)]
