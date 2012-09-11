#!/usr/bin/env python

import urllib2
import urllib
import datetime
import logging
from nws import dwml_parser
from nws.forecast import *

def main():
    dwml = request_dwml_grid(45.5508, -122.738, 50.0, 50.0, 50.0)
    parser = dwml_parser.DWML_Parser(dwml)
    forecast_grid = parser.generate_forecast_grid()
    print_forecast(forecast_grid)

def request_dwml_grid(lat, lng, lat_distance, lng_distance, resolution):
    url = build_noaa_url(lat, lng, lat_distance, lng_distance, resolution)
    f = urllib2.urlopen(url)
    dwml = f.read()
    return dwml

def build_noaa_url(lat, lng, lat_distance, lng_distance, resolution):
    noaaURL = "http://graphical.weather.gov/xml/sample_products/browser_interface/ndfdBrowserClientByDay.php"
    paramaters = {"centerPointLat" : lat, \
                  "centerPointLon" : lng, \
                  "distanceLat" : lat_distance, \
                  "distanceLon" : lng_distance, \
                  "resolutionSquare" : resolution, \
                  "numDays" : 7}
    encoded_params = urllib.urlencode(paramaters)
    nonencoded_params = "&format=24+hourly" # api does not want '+' urlencoded 
    url_query_string = encoded_params + nonencoded_params
    url = noaaURL + "?" + url_query_string 
    return url


# TODO: make this a member func of forecast_grid?
def print_forecast(forecast_grid):
    for forecast in forecast_grid:
        print "Forecast for Lat:%s, Lon:%s" % (forecast.coordinates.lat, forecast.coordinates.lng)
        for day, weather in forecast.daily_weather.items():
            print "%s: High %s, Low %s, Condition %s " % (str(day), weather.high, weather.low, weather.condition) 
        print "\n"
        

if __name__ == "__main__":
    main()