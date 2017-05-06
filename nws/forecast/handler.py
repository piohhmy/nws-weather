import os
import sys
import json
import logging

from lib.dwml_parser import DWML_Parser
from lib.geojson_parser import GeoJsonParser
from lib import weather_proxy
from lib import noaa_proxy
from lib.forecast import Coordinates, ForecastSerializerV2, ForecastSerializerV1

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def get(event, context):
    print(event)
    coord = Coordinates(event['lat'], event['lng'])
    isV2 = event['Accept'] == "application/vnd.weatherhunt.v2+json"
    return geojson_forecast(coord) if isV2 else dwml_forecast(coord)

def dwml_forecast(coord):
    new_forecast_dwml = noaa_proxy.request_dwml_grid_points([coord])
    logger.debug('dwml new forecasts: %s', new_forecast_dwml)
    parser = DWML_Parser(new_forecast_dwml, False)
    new_forecasts = parser.generate_forecast_grid()
    print new_forecasts
    return genResponse(new_forecasts, ForecastSerializerV1)

def geojson_forecast(coord):
    new_forecast_geojson = weather_proxy.get_forecast_for(coord.lat, coord.lng)
    new_forecasts = GeoJsonParser(new_forecast_geojson).parse()
    return genResponse([new_forecasts], ForecastSerializerV2)

def genResponse(forecasts, serializer):
    return_content = json.dumps(forecasts, cls=serializer)
    logger.debug('new forecasts: %s', return_content)
    return json.loads(return_content)
