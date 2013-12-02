from pymongo import MongoClient, GEOSPHERE
from nws import forecast
import json
import os

client = MongoClient(os.getenv('MONGOLAB_URI', 'mongodb://localhost:27017/weather_hunter'))
db = client.get_default_database()
db.forecasts.create_index([("loc", GEOSPHERE)])


def find(coord, max_distance):
	collection = db.forecasts
	for result in collection.find({'loc': {'$near':{'$geometry': {'type':'Point', 'coordinates': [float(coord.lng), float(coord.lat)]}, '$maxDistance':max_distance}}}).limit(1):
		lng, lat = result["loc"]["coordinates"]
		fore = forecast.Forecast(forecast.Coordinates(lat, lng))
		fore.daily_weather = result["daily_weather"]
		return fore
	return None


def insert(new_forecast):
	collection = db.forecasts
	daily_weather_doc = json.loads(json.dumps(new_forecast.daily_weather, cls=forecast.ForecastSerializer))
	forecast_doc = {'loc':{'type':'Point', 'coordinates':[float(new_forecast.coordinates.lng), float(new_forecast.coordinates.lat)]}, 'daily_weather':daily_weather_doc}
	collection.insert(forecast_doc)
