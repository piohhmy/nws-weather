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


class Weather:
    def __init__(self, high, low, condition):
        self.high = high
        self.low = low
        self.condition = condition
        self.unit = "Fahrenheit"
        
