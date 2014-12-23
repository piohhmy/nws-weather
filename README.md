nws-weather
===========

Simplified interface for interacting with the weather APIs provided by the 
National Weather Service (NWS)

[ ![Codeship Status for piohhmy/nws-weather](https://www.codeship.io/projects/826e75f0-4376-0131-40fb-22591c88ea21/status)](https://www.codeship.io/projects/10696)

## Get a Grid of Weather Forecasts
Supply two pairs of coordinates to make a rectangle and receive weather 
forecasts for a number of points within that plane

### Resource URL
```
GET weatherhunter/v3/gridlist
```

### Query Parameters
| name    | description  										 | required? |
|---------|------------------------------------------------------|-----------|
|  lat1   | latitude of NW bound								 | yes       | 
|  lng1   | longitude of NW bound 								 | yes       | 
|  lat2   | latitude of SE bound  								 | yes       |
|  lng2   | longitude of SE bound                                | yes       | 
|  points | number of points to return within the requested area | no        |

Note: The maximum number of points to be returned is 150


### Response
```
[
    {
        "coordinates": {
            "lng": "-122.66",
            "lat": "45.55"
        },
        "daily_weather": {
            "2014-12-28": {
                "unit": "Fahrenheit",
                "high": 47,
                "low": 33,
                "condition": "Chance Rain Showers"
            },
            "2014-12-23": {
                "unit": "Fahrenheit",
                "high": 55,
                "low": 43,
                "condition": "Rain"
            },
            "2014-12-26": {
                "unit": "Fahrenheit",
                "high": 48,
                "low": 39,
                "condition": "Chance Rain"
            },
            "2014-12-27": {
                "unit": "Fahrenheit",
                "high": 46,
                "low": 38,
                "condition": "Chance Rain"
            },
            "2014-12-24": {
                "unit": "Fahrenheit",
                "high": 46,
                "low": 37,
                "condition": "Rain"
            },
            "2014-12-25": {
                "unit": "Fahrenheit",
                "high": 45,
                "low": 40,
                "condition": "Chance Rain Showers"
            }
        }
    },
    ...
 ]
 ```

