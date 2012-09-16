#!/usr/bin/env python

from nws.forecast import *
import unittest
import json

class TestForecast(unittest.TestCase):
    def test_add_daily_forecast(self):
        forecast = Forecast(Coordinates(127.13, 23.53))
        todays_weather = Weather(70, 40, "sunny")
        forecast.daily_weather[datetime.date.today()] = todays_weather
        self.assertEqual(forecast.daily_weather[datetime.date.today()], todays_weather)
    
    def test_forecast_to_json(self):
        forecast = Forecast(Coordinates(127.13, 23.53))
        todays_weather = Weather("70", "40", "sunny")
        forecast.daily_weather[datetime.date.today().isoformat()] = todays_weather

        print json.dumps(forecast, cls=ForecastSerializer)

class TestCoordinates(unittest.TestCase):
    def setUp(self):
        self.latitude = 127.23
        self.longitude = 45.2
        
    def test_coordinates_get_latitude(self):
        coors = Coordinates(self.latitude, self.longitude)
        self.assertEqual(self.latitude, coors.lat)

    def test_coordinates_get_longitude(self):
        coors = Coordinates(self.latitude, self.longitude)
        self.assertEqual(self.longitude, coors.lng)

    def test_coordinates_equality(self):
        coors1 = Coordinates(self.latitude, self.longitude)
        coors2 = Coordinates(self.latitude, self.longitude)
        self.assertEqual(coors1, coors2)

    def test_weather_equality(self):
        weather1 = Weather(10, 20, "sunny")
        weather2 = Weather(10, 20, "sunny")
        self.assertEqual(weather1, weather2)
        

if __name__ == '__main__':
    unittest.main(exit=False)
    
