#!/usr/bin/env python
import datetime
import noaa_parser
import unittest
from forecast import *

class TestForecast(unittest.TestCase):
    def setUp(self):
        f = open('sample_grid_response.xml')	
    	dwml = f.read()
    	self.forecasts = noaa_parser.parse_dwml(dwml)
	
    def test_static_dwml_is_not_null(self):
    	self.assertIsNotNone(self.forecasts)

    def test_static_dwml_contains_a_forecast(self):
    	self.assertIsInstance(self.forecasts[0], Forecast)

    def test_static_dwml_contains_weather_condition(self):
        requested_date = datetime.date(2012, 9, 1)
        print "This is the daily weather: " + str(self.forecasts[0].daily_weather)
    	self.assertIsInstance(self.forecasts[0].daily_weather[requested_date], Weather)

if __name__ == '__main__':
    unittest.main(exit=False)
   
