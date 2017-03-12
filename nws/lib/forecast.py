#!/usr/bin/env python

import unittest
import datetime
import json
import math

class Coordinates:
    def __init__(self, lat, lng):
        self.lat = lat
        self.lng = lng

    def miles_from(self, other):
        earth_radius_miles = 3960
        return distance_on_unit_sphere(self.lat, self.lng, other.lat, other.lng)  * earth_radius_miles

    def km_from(self, other):
        earth_radius_km = 6371
        return distance_on_unit_sphere(self.lat, self.lng, other.lat, other.lng)  * earth_radius_km

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
        self.daily_weather = []

    def add(self, weather):
        self.daily_weather.append(weather)

    def __str__(self):
        return_str =  "Forecast for Lat:%s, Lon:%s" % \
                      (self.coordinates.lat, self.coordinates.lng)
        for weather in self.daily_weather:
            return_str += "\n%s: High %s, Low %s, Condition %s " % \
                          (str(weather.date), weather.high, weather.low, weather.condition)
        return return_str


class ForecastSerializerV1(json.JSONEncoder):
    """ JSON serializes Forecast objects """
    def default(self, obj):
        if isinstance(obj, (Coordinates, Weather)):
            return obj.__dict__
        elif isinstance(obj, Forecast):
            v1Forecast = {day.date: day for day in obj.daily_weather}
            obj.daily_weather = v1Forecast
            return obj.__dict__
        else:
            json.JSONEncoder.default(self, obj)

class ForecastSerializerV2(json.JSONEncoder):
    """ JSON serializes Forecast objects """
    def default(self, obj):
        if isinstance(obj, (Coordinates, Weather, Forecast)):
            return obj.__dict__
        else:
            json.JSONEncoder.default(self, obj)


class Weather:
    def __init__(self, date, high, low, condition):
        self.date = date
        self.high = high
        self.low = low
        self.condition = condition

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
                and self.__dict__ == other.__dict__)
    def __ne__(self, other):
        return not self.__eq__(other)


def distance_on_unit_sphere(lat1, long1, lat2, long2):
    # Convert latitude and longitude to
    # spherical coordinates in radians.
    degrees_to_radians = math.pi/180.

    # phi = 90 - latitude
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians

    # theta = longitude
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians

    # Compute spherical distance from spherical coordinates.

    # For two locations in spherical coordinates
    # (1, theta, phi) and (1, theta, phi)
    # cosine( arc length ) =
    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length

    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) +
           math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )

    # Remember to multiply arc by the radius of the earth
    # in your favorite set of units to get length.
    return arc
