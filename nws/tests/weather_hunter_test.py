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
    def test_api(self):
        thread.start_new_thread(nws.weather_hunter.start_server, ())
        curr_dir = os.path.dirname(os.path.realpath(__file__))
        f = open(curr_dir + '/sample_grid_response.xml')	
        dwml = f.read()
        time.sleep(.01)
        mock_dwml_request = mock.Mock(return_value=dwml)
        nws.noaa_proxy.request_dwml_grid = mock_dwml_request
        url = "http://localhost:8080/weatherhunter/gridlist.svc?lat=127.13&lng=23.53&distance=100"
        urllib.urlopen(url)

        mock_dwml_request.assert_called_with(127.13, 23.53, 100, 100) 
        
if __name__ == '__main__':
    unittest.main(exit=False)
