#!/usr/bin/env python

import xml.etree.ElementTree as ET
import datetime
from lib.forecast import Coordinates, Forecast, Weather
from itertools import izip_longest
from functools import partial



class DWML_Parser:
    def __init__(self, dwml, parsePartialEntries=False):
        self.root  = ET.fromstring(dwml)
        self.parsePartialEntries = parsePartialEntries

    def generate_forecast_grid(self):
        coordinates = self.get_coordinate_list()
        forecast_dates = self.get_forecast_dates()
        forecasts = self.get_weather_forecasts(forecast_dates)
        return self.munge_forecast_grid(coordinates, forecasts)

    def get_coordinate_list(self):
        coordinates = []
        for point_node in self.root.iter("point"):
            lat = point_node.attrib["latitude"]
            lng = point_node.attrib["longitude"]
            coordinates.append(Coordinates(lat,lng))
        return coordinates

    def get_forecast_dates(self):
        forecast_dates = []
        for start_time_node in self.root.iter("start-valid-time"):
            isoDate = parseIsoDate(start_time_node.text)
            if isoDate not in forecast_dates:
                forecast_dates.append(isoDate)
        return forecast_dates

    def get_weather_forecasts(self, forecast_dates):
        weather_list= []
        for forecast_node in self.root.iter("parameters"):
            max_temps, min_temps = self.get_daily_temperatures(forecast_node)
            daily_conditions = self.get_daily_conditions(forecast_node)
            daily_weather = self.munge_daily_weather(forecast_dates, max_temps, min_temps, daily_conditions)
            weather_list.append(daily_weather)
        return weather_list

    def get_daily_temperatures(self, forecast_node):
        max_temps = []
        min_temps = []
        for temperature_node in forecast_node.iter("temperature"):
            if temperature_node.attrib["type"] == "maximum":
                for daily_max_node in temperature_node.iter("value"):
                    if daily_max_node.text is not None:
                        max_temps.append(int(daily_max_node.text))
            else:
                for daily_min_node in temperature_node.iter("value"):
                    if daily_min_node.text is not  None:
                        min_temps.append(int(daily_min_node.text))
        return max_temps, min_temps

    def get_daily_conditions(self, forecast_node):
        daily_conditions = []
        for daily_condition_node in forecast_node.iter("weather-conditions"):
            if "weather-summary" in daily_condition_node.attrib:
                daily_conditions.append(daily_condition_node.attrib["weather-summary"])
            else:
                break
        return daily_conditions

    def munge_daily_weather(self, forecast_dates, max_temps, min_temps, daily_conditions):
        daily_weather = []
        zipper = partial(izip_longest, fillvalue=None) if self.parsePartialEntries else zip
        for date, max_temp, min_temp, condition in zipper(forecast_dates,max_temps, min_temps, daily_conditions):
            daily_weather.append(Weather(date, max_temp, min_temp, condition))
        return daily_weather

    def munge_forecast_grid(self, coordinates, weather_list):
        forecast_grid = []
        for coord, weather in zip(coordinates, weather_list):
            forecast = Forecast(coord)
            forecast.daily_weather = weather
            forecast_grid.append(forecast)
        return forecast_grid

def transform_latlong_str(latlon):
    lat,lng = latlon.split(',')
    return Coordinates(float(lat), float(lng))


def latlonlist_transform(dwml):
    et = ET.fromstring(dwml)
    elem = et.find('latLonList').text.strip()
    coord_pairs = elem.split(' ')
    lat_lon_list = map(transform_latlong_str, coord_pairs)
    return lat_lon_list

def parseIsoDate(datestr):
    excess_time_info_index = datestr.rfind('-')
    datestr = datestr[0:excess_time_info_index]
    dt = datetime.datetime.strptime(datestr, "%Y-%m-%dT%H:%M:%S")
    return dt.date().isoformat()
