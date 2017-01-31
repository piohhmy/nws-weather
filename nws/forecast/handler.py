import os
import sys
import json
import logging

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "../vendored"))
from lib.dwml_parser import DWML_Parser
from lib import noaa_proxy
from lib.forecast import Coordinates, ForecastSerializer

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def get(event, context):
    print(event)
    coord = Coordinates(event['lat'], event['lng'])
    supportPartialForecasts = event['Accept'] == "application/vnd.weatherhunt.v2+json"

    return forecast(coord, supportPartialForecasts )

def forecast(coord, supportPartialForecasts):
    new_forecast_dwml = noaa_proxy.request_dwml_grid_points([coord])
    logger.debug('dwml new forecasts: %s', new_forecast_dwml)
    parser = DWML_Parser(new_forecast_dwml, supportPartialForecasts)
    new_forecasts = parser.generate_forecast_grid()

    return_content = json.dumps(new_forecasts, cls=ForecastSerializer)

    logger.debug('new forecasts: %s', return_content)

    return json.loads(return_content)
