#!/usr/bin/env python
import datetime
import noaa_parser
import unittest
from forecast import *
"""
Point 1 data from sample_grid_response.xml

<point latitude="45.01" longitude="-123.20"/>
<start-valid-time>2012-08-31T06:00:00-07:00</start-valid-time>
<end-valid-time>2012-09-01T06:00:00-07:00</end-valid-time>
<name>Daily Maximum Temperature</name>
<value>78</value>
<value>78</value>
<value>79</value>
<value>81</value>
<value>82</value>
<value>88</value>
<value>86</value>
</temperature>
<temperature type="minimum" units="Fahrenheit" time-layout="k-p24h-n7-1">
<name>Daily Minimum Temperature</name>
<value>45</value>
<value>46</value>
<value>49</value>
<value>48</value>
<value>52</value>
<value>52</value>
<value>54</value>
<weather time-layout="k-p24h-n7-1">
<name>Weather Type, Coverage, and Intensity</name>
<weather-conditions weather-summary="Mostly Sunny"/>
<weather-conditions weather-summary="Mostly Sunny"/>
<weather-conditions weather-summary="Partly Sunny"/>
<weather-conditions weather-summary="Mostly Sunny"/>
<weather-conditions weather-summary="Mostly Sunny"/>
<weather-conditions weather-summary="Mostly Sunny"/>
<weather-conditions weather-summary="Mostly Sunny"/>
</weather>
"""
class TestForecast(unittest.TestCase):
    def setUp(self):
        f = open('sample_grid_response.xml')	
    	dwml = f.read()
    	self.forecasts = noaa_parser.parse_dwml(dwml)
	
    def test_static_dwml_is_not_null(self):
    	self.assertIsNotNone(self.forecasts)

    def test_static_dwml_contains_a_forecast(self):
    	self.assertIsInstance(self.forecasts[0], Forecast)

    def test_static_dwml_contains_weather_condition_for_date(self):
        requested_date = datetime.date(2012, 8, 31)
    	self.assertIsInstance(self.forecasts[0].daily_weather[requested_date], Weather)

    def test_static_dwml_contains_correct_weather_data(self):
        requested_date = datetime.date(2012, 8, 31)
        actual_weather = self.forecasts[0].daily_weather[requested_date]
        expected_weather = Weather(78, 45, "Mostly Sunny")
        self.assertEqual(actual_weather, expected_weather) 

if __name__ == '__main__':
    unittest.main(exit=False)
   
