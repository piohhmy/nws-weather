#!/usr/bin/env python

import noaa_parser
import unittest
from forecast import *

class TestForecast(unittest.TestCase):
    def test_static_dwml_is_not_null(self):
        f = open('sample_grid_response.xml')	
	dwml = f.read()
	forecasts = noaa_parser.parse_dwml(dwml)
	self.assertIsNotNone(forecasts)

    def test_static_dwml_contains_a_forecast(self):
        f = open('sample_grid_response.xml')	
	dwml = f.read()
	forecasts = noaa_parser.parse_dwml(dwml)
	self.assertIsInstance(forecasts[0], Forecast)

if __name__ == '__main__':
    unittest.main(exit=False)
   
