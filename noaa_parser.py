#!/usr/bin/env python

import urllib2
import urllib
import xml.dom.minidom as minidom
import time
import logging
from forecast import *

def main():
    dwml = request_dwml_grid(45.5508, -122.738, 50.0, 50.0, 50.0)
    print dwml
    forecast_grid = parse_dwml(dwml)


def request_dwml_grid(lat, lng, lat_distance, lng_distance, resolution):
    noaaURL = "http://graphical.weather.gov/xml/sample_products/browser_interface/ndfdBrowserClientByDay.php"
    paramaters = {"centerPointLat" : lat, "centerPointLon" : lng, "distanceLat" : lat_distance, "distanceLon" : lng_distance, "resolutionSquare" : resolution, "numDays" : 7}
    url_query_string = urllib.urlencode(paramaters) + "&format=24+hourly" # urlencoding the '+' in format param causes an error, explicitly add it
    url = noaaURL + "?" + url_query_string 
    f = urllib2.urlopen(url)
    print url
    dwml = f.read()
    return dwml

def parse_dwml(dwml):
    doc = minidom.parseString(dwml)
    forecasts = doc.getElementsByTagName("parameters")
    points = doc.getElementsByTagName("point")
    start_times = doc.getElementsByTagName("start-valid-time")
    end_times = doc.getElementsByTagName("end-valid-time")
   

    forecast_grid = []

    for point_index in range(len(points)):
        lat = points[point_index].getAttribute("latitude")
        lng = points[point_index].getAttribute("longitude")
        print "Latitude: " + lat
        print "Longitude: " + lng
        forecast = Forecast(Coordinates(lat, lng))
        temperatures = forecasts[point_index].getElementsByTagName("temperature")
        daily_highs = temperatures[0].getElementsByTagName("value")
        daily_lows = temperatures[1].getElementsByTagName("value")
        for daily_index in range(len(daily_highs)):
            # TODO: Add this data into forecast object
            start_time = start_times[daily_index].firstChild.nodeValue
            end_time = end_times[daily_index].firstChild.nodeValue
            print start_time
            print end_time
            if daily_highs[daily_index].hasChildNodes() == True:
                print "High: " + daily_highs[daily_index].firstChild.nodeValue
            if daily_lows[daily_index].hasChildNodes() == True:
                print "Low: " + daily_lows[daily_index].firstChild.nodeValue
            conditions = forecasts[point_index].getElementsByTagName("weather-conditions")
            print "Conditions: " + conditions[daily_index].getAttribute('weather-summary')
            print "\n"
        forecast_grid.append(forecast)
        print "-------------"
        
        
if __name__ == "__main__":
    main()
