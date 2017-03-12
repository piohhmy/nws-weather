import datetime
import dateutil.parser
import itertools
from lib.forecast import Coordinates, Forecast, Weather


class GeoJsonParser:
    def __init__(self, geojson):
        self.geojson = geojson

    def _getDateFromPeriod(self, period):
        return dateutil.parser.parse(period['startTime']).date()

    def parse(self):
        geocoords = self.geojson['geometry']['coordinates']
        coords = Coordinates(geocoords[1], geocoords[0])
        periods = self.geojson['properties']['periods']
        forecast = Forecast(coords)
        for day, forecasts in itertools.groupby(periods, key=self._getDateFromPeriod):
            forecasts = list(forecasts)
            high = next((f['temperature'] for f in forecasts if f['isDaytime']), None)
            low = next((f['temperature'] for f in forecasts if not f['isDaytime']), None)
            condition = forecasts[0]['shortForecast']
            forecast.add(Weather(day.isoformat(), high, low, condition))
        return forecast
