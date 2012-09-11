#!/usr/bin/env python

import unittest
import datetime

class Coordinates:
    def __init__(self, lat, lng):      
        self.lat = lat
        self.lng = lng

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
                and self.__dict__ == other.__dict__)
    def __ne__(self, other):
        return not self.__eq__(other)
        

class Forecast:
    def __init__(self, coordinates):
        self.coordinates = coordinates
        self.daily_weather = {}
    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)
    def __str__(self):
        return_str =  "Forecast for Lat:%s, Lon:%s" % (self.coordinates.lat, self.coordinates.lng)
        for day, weather in self.daily_weather.items():
            return_str +=  "\n%s: High %s, Low %s, Condition %s " % (str(day), weather.high, weather.low, weather.condition) 
        return return_str


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

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)
