#!/usr/bin/env python

import urllib2
import urllib
import xml.dom.minidom as minidom
import datetime
import logging
from forecast import *

def main():
    dwml = request_dwml_grid(45.5508, -122.738, 50.0, 50.0, 50.0)
    print dwml
    forecast_grid = parse_dwml(dwml)
    print_forecast(forecast_grid)

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
        forecast = Forecast(Coordinates(lat, lng))
        temperatures = forecasts[point_index].getElementsByTagName("temperature")
        daily_highs = temperatures[0].getElementsByTagName("value")
        daily_lows = temperatures[1].getElementsByTagName("value")
        for daily_index in range(len(daily_highs)):
            if daily_highs[daily_index].hasChildNodes() == True:
                high = daily_highs[daily_index].firstChild.nodeValue
            if daily_lows[daily_index].hasChildNodes() == True:
                low = daily_lows[daily_index].firstChild.nodeValue
            conditions = forecasts[point_index].getElementsByTagName("weather-conditions")
            condition_summary = conditions[daily_index].getAttribute('weather-summary')
            weather = Weather(int(high), int(low), condition_summary)
            start_time = start_times[daily_index].firstChild.nodeValue
            end_time = end_times[daily_index].firstChild.nodeValue
            dt = datetime.datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S-07:00")
            forecast.daily_weather[dt.date()] = weather
        forecast_grid.append(forecast)
    return forecast_grid
        
def print_forecast(forecast_grid):
    for forecast in forecast_grid:
        print "Forecast for Lat:%s, Lon:%s" % (forecast.coordinates.lat, forecast.coordinates.lng)
        for day, weather in forecast.daily_weather.items():
            print "%s: High %s, Low %s, Condition %s " % (str(day), weather.high, weather.low, weather.condition) 

        print "\n"
        
if __name__ == "__main__":
    main()
