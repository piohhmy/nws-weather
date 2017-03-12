#!/usr/bin/env python
import datetime
from lib import geojson_parser
from lib.forecast import Coordinates
import unittest
from lib.forecast import *
from nose.tools import *
import json
import os
"""
{
  "@context": [
  ],
  "type": "Feature",
  "geometry": {
    "type": "Point",
    "coordinates": [
      -94.6716,
      45.0693
    ]
  },
  "properties": {
    "updated": "2017-03-11T14:41:59+00:00",
    "periods": [
      {
        "number": 1,
        "name": "Today",
        "startTime": "2017-03-11T10:00:00-06:00",
        "endTime": "2017-03-11T18:00:00-06:00",
        "isDaytime": true,
        "temperature": 22,
        "windSpeed": "7 mph",
        "windDirection": "N",
        "icon": "https://api.weather.gov/icons/land/day/bkn?size=medium",
        "shortForecast": "Mostly Cloudy",
        "detailedForecast": "Mostly cloudy, with a high near 22. North wind around 7 mph.",
        "detailedForecastSI": "Mostly cloudy, with a high near -6. North wind around 11 km/h."
      },
"""
class TestGeoJsonParser(unittest.TestCase):
    def setUp(self):
        curr_dir = os.path.dirname(os.path.realpath(__file__))
        f = open(curr_dir + '/sample_geojson_point_response.json')
        geojson = json.loads(f.read())
        parser = geojson_parser.GeoJsonParser(geojson)
        self.forecast = parser.parse()

    def test_returns_a_forecast(self):
        self.assertIsInstance(self.forecast, Forecast)

    def test_returns_a_weather_condition(self):
        self.assertIsInstance(self.forecast.daily_weather[0], Weather)

    def test_returns_correct_weather_data(self):
        expected_date = datetime.date(2017, 3, 11).isoformat()
        actual_weather = self.forecast.daily_weather[0]
        expected_weather = Weather(expected_date, 22, 9, "Mostly Cloudy")
        self.assertEqual(actual_weather, expected_weather)

    def test_ignores_compound_short_forecasts(self):
        expected_date = datetime.date(2017, 3, 13).isoformat()
        actual_weather = self.forecast.daily_weather[2]
        expected_weather = Weather(expected_date, 26, 9, "Slight Chance Snow")
        self.assertEqual(actual_weather, expected_weather)

    def test_is_serializable_with_serializationV2(self):
        j = json.loads(json.dumps([self.forecast], sort_keys=True, indent=4,
                cls=ForecastSerializerV2))
        forecast = j[0]
        self.assertEqual(len(forecast['daily_weather']), 7)
        self.assertEqual(forecast['daily_weather'][0]['date'], '2017-03-11')


class TestGeoJsonParserWithMissingDayForecast(unittest.TestCase):
    def setUp(self):
        curr_dir = os.path.dirname(os.path.realpath(__file__))
        f = open(curr_dir + '/sample_geojson_point_response_no_day_forecast.json')
        geojson = json.loads(f.read())
        parser = geojson_parser.GeoJsonParser(geojson)
        self.forecast = parser.parse()

    def test_returns_correct_weather_data_on_missing_day_forecast(self):
        expected_date = datetime.date(2017, 3, 11).isoformat()
        actual_weather = self.forecast.daily_weather[0]
        expected_weather = Weather(expected_date, None, 9, "Mostly Cloudy")
        self.assertEqual(actual_weather, expected_weather)

    def test_returns_correct_weather_data_on_missing_night_forecast(self):
        expected_date = datetime.date(2017, 3, 18).isoformat()
        actual_weather = self.forecast.daily_weather[7]
        expected_weather = Weather(expected_date, 45, None, "Mostly Sunny")
        self.assertEqual(actual_weather, expected_weather)



if __name__ == '__main__':
    unittest.main(exit=False)
