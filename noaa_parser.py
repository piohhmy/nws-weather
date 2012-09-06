#!/usr/bin/env python

import urllib2
import urllib
import xml.etree.ElementTree as ET
import datetime
import logging
from forecast import *

def main():
    dwml = request_dwml_grid(45.5508, -122.738, 50.0, 50.0, 50.0)
    parser = DWML_Parser(dwml)
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


def print_forecast(forecast_grid):
    for forecast in forecast_grid:
        print "Forecast for Lat:%s, Lon:%s" % (forecast.coordinates.lat, forecast.coordinates.lng)
        for day, weather in forecast.daily_weather.items():
            print "%s: High %s, Low %s, Condition %s " % (str(day), weather.high, weather.low, weather.condition) 
        print "\n"
        
class DWML_Parser:
    def __init__(self, dwml):
        self.root  = ET.fromstring(dwml)

    def generate_forecast_grid(self):
        coordinates = self.get_coordinate_list()
        forecast_dates = self.get_forecast_dates()
        forecasts = self.get_weather_forecasts()
        return self.munge_forecast_grid(coordinates, forecast_dates, forecasts)

    def get_coordinate_list(self):
        coordinates = []
        for point in self.root.iter("point"):
            lat = point.attrib["latitude"]            
            lng = point.attrib["longitude"]
            coordinates.append(Coordinates(lat,lng))
        return coordinates

    def get_forecast_dates(self):
        forecast_dates = []
        for start_time in self.root.iter("start-valid-time"):
            time = start_time.text
            dt = datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%S-07:00")
            forecast_dates.append(dt.date())
        return forecast_dates

    def get_weather_forecasts(self):
        forecasts = []
        for forecast in self.root.iter("parameters"):
            max_temps = []
            min_temps = []
            daily_conditions = []
            for temperature_set in forecast.iter("temperature"):
                if temperature_set.attrib["type"] == "maximum":
                    for daily_max in temperature_set.iter("value"):
                        max_temps.append(int(daily_max.text))
                else:
                    for daily_min in temperature_set.iter("value"):
                        min_temps.append(int(daily_min.text))
            for daily_condition in forecast.iter("weather-conditions"):
                daily_conditions.append(daily_condition.attrib["weather-summary"])
                

            daily_weather = []
            for max_temp, min_temp, condition in zip(max_temps, min_temps, daily_conditions):
                daily_weather.append(Weather(max_temp, min_temp, condition))
            forecasts.append(daily_weather)
        return forecasts

    def munge_forecast_grid(self, coordinates, forecast_dates, forecasts):
        forecast_grid = []
        for coord, forecast in zip(coordinates, forecasts):
            new_forecast = Forecast(coord)
            for start_time, weather in zip(forecast_dates, forecast):
               new_forecast.daily_weather[start_time] = weather
            forecast_grid.append(new_forecast)
        return forecast_grid

if __name__ == "__main__":
    main()
