#!/usr/bin/env python

from nws.forecast import *
import unittest
import urllib
import mock
import nws.noaa_proxy
import nws.weather_hunter
import thread
import time
import os

class TestWeatherHunter(unittest.TestCase):
    def setUp(self):
        nws.weather_hunter.app.config['TESTING'] = True
        self.app = nws.weather_hunter.app.test_client()
        curr_dir = os.path.dirname(os.path.realpath(__file__))
        f = open(curr_dir + '/sample_grid_response.xml')
        dwml = f.read()
        self.mock_noaa_proxy_dwml_request = mock.Mock(return_value=dwml)
        nws.noaa_proxy.request_dwml_grid = self.mock_noaa_proxy_dwml_request

    def test_gridlist_calls(self):
        route = "/weatherhunter/v1/gridlist?lat=127.13&lng=23.53&distance=100"
        rv = self.app.get(route)

        self.mock_noaa_proxy_dwml_request.assert_called_with(127.13, 23.53, 100, 100, 50)

    def test_gridlist_returns_json(self):
        route = "/weatherhunter/v1/gridlist?lat=127.13&lng=23.53&distance=100"
        rv = self.app.get(route)

        self.assertEqual(rv.headers['content-type'], "application/json")

    def test_sun_request_filtered_by_date(self):
        route = "/weatherhunter/v1/sun?lat=127.13&lng=23.53&distance=100&days_from_today=0"
        rv = self.app.get(route)


    def test_sun_request_without_date(self):
        route = "/weatherhunter/v1/sun?lat=127.13&lng=23.53&distance=100"
        rv = self.app.get(route)

if __name__ == '__main__':
    unittest.main(exit=False)
