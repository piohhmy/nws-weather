import os
import sys
import json
import logging

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "../vendored"))
from lib.dwml_parser import DWML_Parser
from lib import noaa_proxy
from lib.forecast import Coordinates, ForecastSerializerV2, ForecastSerializerV1

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def get(event, context):
    print(event)
    coord = Coordinates(event['lat'], event['lng'])
    isV2 = event['Accept'] == "application/vnd.weatherhunt.v2+json"

    return forecast(coord, isV2)

def forecast(coord, isV2):
    new_forecast_dwml = noaa_proxy.request_dwml_grid_points([coord])
    logger.debug('dwml new forecasts: %s', new_forecast_dwml)
    parser = DWML_Parser(new_forecast_dwml, isV2)
    new_forecasts = parser.generate_forecast_grid()
    print new_forecasts
    forecastSerializer = ForecastSerializerV2 if isV2 else ForecastSerializerV1
    return_content = json.dumps(new_forecasts, cls=forecastSerializer)

    logger.debug('new forecasts: %s', return_content)

    return json.loads(return_content)
