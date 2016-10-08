from pymongo import MongoClient, GEOSPHERE, ASCENDING
from lib import forecast
import json
import os
import datetime

class MongoRepo(object):
	client = MongoClient(os.getenv('MONGOLAB_URI', 'mongodb://localhost:27017/weather_hunter'))
	db = client.get_default_database()
	db.forecasts.ensure_index([("loc", GEOSPHERE)])
	db.forecasts.ensure_index("createdAt", expireAfterSeconds=3600)
	collection = db.forecasts

	@staticmethod
	def find(coord, max_distance):
		for result in MongoRepo.collection.find({'loc': {'$near':{'$geometry': {'type':'Point', 'coordinates': [float(coord.lng), float(coord.lat)]}, '$maxDistance':max_distance}}}).limit(1):
			lng, lat = result["loc"]["coordinates"]
			fore = forecast.Forecast(forecast.Coordinates(lat, lng))
			fore.daily_weather = result["daily_weather"]
			return fore
		return None


	@staticmethod
	def insert(new_forecast):
		daily_weather_doc = json.loads(json.dumps(new_forecast.daily_weather, cls=forecast.ForecastSerializer))
		forecast_doc = {'createdAt': datetime.datetime.utcnow(),
		                'loc':{
		                   'type':'Point',
		                   'coordinates':[float(new_forecast.coordinates.lng), float(new_forecast.coordinates.lat)]
		                   },
		                'daily_weather':daily_weather_doc
		                }
		MongoRepo.collection.insert(forecast_doc)

	@staticmethod
	def empty():
		MongoRepo.collection.remove()
