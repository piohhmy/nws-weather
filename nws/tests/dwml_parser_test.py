#!/usr/bin/env python
import datetime
from lib import dwml_parser
from lib.forecast import Coordinates
import unittest
from lib.forecast import *
from nose.tools import *
import json
import os
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
        curr_dir = os.path.dirname(os.path.realpath(__file__))
        f = open(curr_dir + '/sample_grid_response.xml')
        dwml = f.read()
        parser = dwml_parser.DWML_Parser(dwml)
        self.forecasts = parser.generate_forecast_grid()

    def test_static_dwml_is_not_null(self):
        self.assertIsNotNone(self.forecasts)

    def test_static_dwml_contains_a_forecast(self):
        self.assertIsInstance(self.forecasts[0], Forecast)

    def test_static_dwml_contains_weather_condition_for_date(self):
        requested_date = datetime.date(2012, 8, 31).isoformat()
        self.assertIsInstance(self.forecasts[0].daily_weather[requested_date], Weather)

    def test_static_dwml_contains_correct_weather_data(self):
        requested_date = datetime.date(2012, 8, 31).isoformat()
        actual_weather = self.forecasts[0].daily_weather[requested_date]
        expected_weather = Weather(78, 45, "Mostly Sunny")
        self.assertEqual(actual_weather, expected_weather)

    def test_static_dwml_contains_forecast_for_multiple_points(self):
        self.assertEqual(len(self.forecasts), 9)

    def test_json_serialization_from_forecast_grid(self):
        print json.dumps(self.forecasts, sort_keys=True, indent=4,
                cls=ForecastSerializer)

class TestPartialForecastsWithNulls(unittest.TestCase):
    def setUp(self):
        curr_dir = os.path.dirname(os.path.realpath(__file__))
        f = open(curr_dir + '/sample_response_with_nulls.xml')
        dwml = f.read()
        parser = dwml_parser.DWML_Parser(dwml, parsePartialEntries=True)
        self.forecasts = parser.generate_forecast_grid()

    def test_static_dwml_contains_weather_data_when_only_high_and_low_are_available(self):
        requested_date = datetime.date(2017, 1, 30).isoformat()
        actual_weather = self.forecasts[0].daily_weather[requested_date]
        expected_weather = Weather(58, 41, None)
        self.assertEqual(actual_weather, expected_weather)

    def test_static_dwml_contains_weather_data_when_only_high_is_available(self):
        requested_date = datetime.date(2017, 1, 31).isoformat()
        actual_weather = self.forecasts[0].daily_weather[requested_date]
        expected_weather = Weather(54, None, None)
        self.assertEqual(actual_weather, expected_weather)

    def test_json_serialization_from_forecast_grid(self):
        print json.dumps(self.forecasts, sort_keys=True, indent=4,
                cls=ForecastSerializer)

class TestCompleteForecastsWithNulls(unittest.TestCase):
    def setUp(self):
        curr_dir = os.path.dirname(os.path.realpath(__file__))
        f = open(curr_dir + '/sample_response_with_nulls.xml')
        dwml = f.read()
        parser = dwml_parser.DWML_Parser(dwml, parsePartialEntries=False)
        self.forecasts = parser.generate_forecast_grid()

    def test_static_dwml_does_not_contain_weather_data_when_only_high_and_low_are_available(self):
        requested_date = datetime.date(2017, 1, 30).isoformat()
        with self.assertRaises(KeyError):
            self.forecasts[0].daily_weather[requested_date]

    def test_static_dwml_does_not_contain_weather_data_when_only_high_is_available(self):
        requested_date = datetime.date(2017, 1, 31).isoformat()
        with self.assertRaises(KeyError):
            self.forecasts[0].daily_weather[requested_date]

    def test_json_serialization_from_forecast_grid(self):
        print json.dumps(self.forecasts, sort_keys=True, indent=4,
                cls=ForecastSerializer)

class TestLatLngList(unittest.TestCase):
    def test_1_coord_returns_list_of_pts(self):
        sample_data1 =\
        """<dwml xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="1.0" xsi:noNamespaceSchemaLocation="http://graphical.weather.gov/xml/DWMLgen/schema/DWML.xsd">
        <latLonList>
        34.986638,-82.027411
        </latLonList>
        </dwml>"""
        result = dwml_parser.latlonlist_transform(sample_data1)
        assert_equal(result, [Coordinates(34.986638,-82.027411)])

    def test_many_coords_returns_list_of_pts(self):
        sample_data1 =\
        """<dwml xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="1.0" xsi:noNamespaceSchemaLocation="http://graphical.weather.gov/xml/DWMLgen/schema/DWML.xsd">
        <latLonList>
        34.986638,-82.02741 35.120891,-82.011661 35.255084,-81.9958721
        </latLonList>
        </dwml>"""
        result = dwml_parser.latlonlist_transform(sample_data1)
        assert_equal(result, [Coordinates(34.986638,-82.02741), Coordinates(35.120891,-82.011661), Coordinates(35.255084,-81.9958721)])
if __name__ == '__main__':
    unittest.main(exit=False)
