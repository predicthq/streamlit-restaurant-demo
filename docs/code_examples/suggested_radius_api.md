## Suggested Radius API

The Suggested Radius API returns a radius that can be used to find attended events around a given location. When looking for events around a business location (such as a store, a hotel, or another business location) a key question is how far should you look for events. For example, should you look at events in a 0.5-mile radius, a 2-mile radius, or a 10-mile radius from your location? The Suggested Radius API answers this question by returning a radius based on a number of factors that can be used to retrieve events around a location.

```python
import requests

response = requests.get(
    url="https://api.predicthq.com/v1/suggested-radius/",
    headers={
      "Authorization": "Bearer $ACCESS_TOKEN",
      "Accept": "application/json"
    },
    params={
        "location.origin": "37.747767,-122.455320",
        "industry": "restaurants",
        "radius_unit": "km"
    }
)

print(response.json())
```

Example response:

```json
{
    "radius": 1.46,
    "radius_unit": "km",
    "location": {
        "lat": "37.747767",
        "lon": "-122.45532"
    }
}
```

Full docs for the Suggested Radius API are available at [https://docs.predicthq.com/resources/suggested-radius](https://docs.predicthq.com/resources/suggested-radius)
