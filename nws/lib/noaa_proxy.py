#!/usr/bin/env python

import urllib2
import urllib
import datetime
import logging
import socket
from lib import dwml_parser

timeout = 30
socket.setdefaulttimeout(timeout)

def request_dwml_grid_points(coords):
    url = build_noaa_url_for_weather_grid_points(coords)
    logging.debug("url: %s", url)
    try:
        f = urllib2.urlopen(url)
        dwml = f.read()
    except urllib2.HTTPError as ex:
        logging.exception(ex.msg)
        raise
    return dwml


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
