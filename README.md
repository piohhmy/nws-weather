nws-weather
===========

Proxy for interacting with the v3 RESTful api and the DWML weather APIs provided by the
National Weather Service (NWS) used by [weatherhunt](http://weatherhunt.com) for iOS

[![CircleCI](https://circleci.com/gh/piohhmy/nws-weather.svg?style=svg&circle-token=bad595b055130a6838bb662d81a1a34479fe24f7)](https://circleci.com/gh/piohhmy/nws-weather)
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
