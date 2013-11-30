#!/usr/bin/env python

import unittest
import datetime
import json

class Coordinates:
    def __init__(self, lat, lng):      
        self.lat = lat
        self.lng = lng

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
                and self.__dict__ == other.__dict__)
    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return "{},{}".format(self.lat, self.lng)

    def __repr__(self):
        return "{},{}".format(self.lat, self.lng)
        

class Forecast:
    def __init__(self, coordinates):
        self.coordinates = coordinates
        self.daily_weather = {}
    def __str__(self):
        return_str =  "Forecast for Lat:%s, Lon:%s" % \
                      (self.coordinates.lat, self.coordinates.lng)
        for day, weather in self.daily_weather.items():
            return_str += "\n%s: High %s, Low %s, Condition %s " % \
                          (str(day), weather.high, weather.low, weather.condition) 
        return return_str

class ForecastSerializer(json.JSONEncoder):
    """ JSON serializes Forecast objects """
    def default(self, obj):
        if isinstance(obj, (Coordinates, Weather, Forecast)):
            return obj.__dict__
        else:
            json.JSONEncoder.default(self, obj)


class Weather:
    def __init__(self, high, low, condition):
        self.high = high
        self.low = low
        self.condition = condition
        self.unit = "Fahrenheit"
        
    def __eq__(self, other):
        return (isinstance(other, self.__class__)
                and self.__dict__ == other.__dict__)
    def __ne__(self, other):
        return not self.__eq__(other)

