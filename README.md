nws-weather
===========

Simplified interface for interacting with the weather APIs provided by the
National Weather Service (NWS)

[ ![Codeship Status for piohhmy/nws-weather](https://www.codeship.com/projects/826e75f0-4376-0131-40fb-22591c88ea21/status)](https://www.codeship.com/projects/10696)

## Get a Weather Forecast for a point

```
GET weather/forecast?lat=145.5&lng=-122.2
Accept: application/vnd.weatherhunt.v2+json
```

### Response
```
[
    {
        "daily_weather": [
            {
                "date": "2017-03-07",
                "high": 48,
                "low": 40,
                "condition": "Rain"
            },
            {
                "date": "2017-03-08",
                "high": 48,
                "low": 40,
                "condition": "Rain"
            },
            {
                "date": "2017-03-09",
                "high": 52,
                "low": 41,
                "condition": "Rain"
            },
            {
                "date": "2017-03-10",
                "high": 49,
                "low": 39,
                "condition": "Chance Rain"
            },
            {
                "date": "2017-03-11",
                "high": 51,
                "low": 41,
                "condition": "Rain Likely"
            },
            {
                "date": "2017-03-12",
                "high": 49,
                "low": 40,
                "condition": "Rain Showers Likely"
            },
            {
                "date": "2017-03-13",
                "high": 50,
                "low": null,
                "condition": "Rain Likely"
            }
        ],
        "coordinates": {
            "lat": "45.50",
            "lng": "-122.60"
        }
    }
]
```
