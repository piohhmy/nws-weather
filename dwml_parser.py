#!/usr/bin/env python

import xml.etree.ElementTree as ET
import datetime
from forecast import *
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
        weather_list= []
        for forecast in self.root.iter("parameters"):
            max_temps, min_temps = self.get_daily_temperatures(forecast)            
            daily_conditions = self.get_daily_conditions(forecast)
            daily_weather = self.munge_daily_weather(max_temps, min_temps, daily_conditions)
            weather_list.append(daily_weather)
        return weather_list

    def get_daily_temperatures(self, forecast):
        max_temps = []
        min_temps = []
        for temperature_set in forecast.iter("temperature"):
            if temperature_set.attrib["type"] == "maximum":
                for daily_max in temperature_set.iter("value"):
                    max_temps.append(int(daily_max.text))
            else:
                for daily_min in temperature_set.iter("value"):
                    min_temps.append(int(daily_min.text))
        return max_temps, min_temps

    def get_daily_conditions(self, forecast):
        daily_conditions = []
        for daily_condition in forecast.iter("weather-conditions"):
            daily_conditions.append(daily_condition.attrib["weather-summary"])
        return daily_conditions

    def munge_daily_weather(self, max_temps, min_temps, daily_conditions):
        daily_weather = []
        for max_temp, min_temp, condition in zip(max_temps, min_temps, daily_conditions):
            daily_weather.append(Weather(max_temp, min_temp, condition))
        return daily_weather

    def munge_forecast_grid(self, coordinates, dates, weather_list):
        forecast_grid = []
        for coord, weather in zip(coordinates, weather_list):
            forecast = Forecast(coord)
            for start_date, weather_per_day in zip(dates, weather):
               forecast.daily_weather[start_date] = weather_per_day
            forecast_grid.append(forecast)
        return forecast_grid
