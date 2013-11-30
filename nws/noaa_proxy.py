#!/usr/bin/env python

import urllib2
import urllib
import datetime
import logging
from nws import dwml_parser
from nws.forecast import *

def main():
    dwml = request_dwml_grid(45.5508, -122.738, 100.0, 100.0, 20.0)
    parser = dwml_parser.DWML_Parser(dwml)
    forecast_grid = parser.generate_forecast_grid()
    print_forecast(forecast_grid)

def request_latlong_list(lat1, lng1, lat2, lng2, resolution):
    url = build_noaa_url_for_latlng_list(lat1, lng1, lat2, lng2, resolution)
    f = urllib2.urlopen(url)
    dwml = f.read()
    return dwml


def request_dwml_grid(lat, lng, lat_distance, lng_distance, resolution=50):
    url = build_noaa_url_for_weather_grid(lat, lng, lat_distance, lng_distance, resolution)
    f = urllib2.urlopen(url)
    dwml = f.read()
    return dwml

def request_dwml_grid_points(coords):
    url = build_noaa_url_for_weather_grid_points(coords)
    logging.info("url: %s", url)
    f = urllib2.urlopen(url)
    dwml = f.read()
    return dwml

def build_noaa_url_for_weather_grid(lat, lng, lat_distance, lng_distance, resolution):
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

def build_noaa_url_for_latlng_list(lat1, lng1, lat2, lng2, resolution):
    noaa_url = "http://graphical.weather.gov/xml/sample_products/browser_interface/ndfdXMLclient.php"
    paramaters = {'listLat1' : lat1, 'listLon1' :lng1, 'listLat2' :lat2, 'listLon2' : lng2, 'resolutionList' : resolution}
    url_query_string = urllib.urlencode(paramaters)
    url = noaa_url + "?" + url_query_string
    return url

def build_noaa_url_for_weather_grid_points(coords):
    comma_delim_coords = ["{},{}".format(coord.lat, coord.lng) for coord in coords]
    coord_str = '+'.join(comma_delim_coords)
    noaaURL = "http://graphical.weather.gov/xml/sample_products/browser_interface/ndfdBrowserClientByDay.php"
    paramaters = { "numDays" : 7}
    encoded_params = urllib.urlencode(paramaters)
    nonencoded_params = "&format=24+hourly&listLatLon=%s" % coord_str # api does not want '+' urlencoded
    url_query_string = encoded_params + nonencoded_params
    url = noaaURL + "?" + url_query_string
    return url

# TODO: make this a member func of forecast_grid?
def print_forecast(forecast_grid):
    print "Printing Forecast"
    for forecast in forecast_grid:
        print forecast
        print "\n"

if __name__ == "__main__":
    main()
