from pymongo import MongoClient, GEOSPHERE
from nws import forecast
import json
client = MongoClient()
db = client.weather_hunter
db.forecasts.create_index([("loc", GEOSPHERE)])


def find(coord, resolution):
	return None

def insert(new_forecast):
	collection = db.forecasts
	daily_weather_doc = json.loads(json.dumps(new_forecast.daily_weather, cls=forecast.ForecastSerializer))
	forecast_doc = {'loc':{'type':'Point', 'coordinates':[float(new_forecast.coordinates.lng), float(new_forecast.coordinates.lat)]}, 'daily_weather':daily_weather_doc}
	collection.insert(forecast_doc)
