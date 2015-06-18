import os
import json
import math
import flask
import geopy
import rollbar
import logging
import datetime
import rollbar.contrib.flask
from geopy.distance import great_circle
from nws import filters
from nws import forecast
from nws import noaa_proxy
from nws import dwml_parser
from nws.forecast import Coordinates
from nws.dwml_parser import DWML_Parser
from nws.mongo_cache import MongoRepo as cache_repo

app = flask.Flask(__name__)

@app.before_first_request
def init_rollbar():
    rollbar.init(os.getenv('ROLLBAR_ACCESS_TOKEN'), 'weatherhunt_api',
        root=os.path.dirname(os.path.realpath(__file__)),
        allow_logging_basic_config=False)

    flask.got_request_exception.connect(rollbar.contrib.flask.report_exception, app)

logging.basicConfig(level=logging.INFO)

@app.route("/")
def index():
    json_resp = json.dumps({'status':'ok'})
    return flask.Response(json_resp, mimetype='application/json')

@app.route("/weatherhunter/v3/gridlist")
def grid_list3():
    lat1 = float(flask.request.args.get("lat1"))
    lng1 = float(flask.request.args.get("lng1"))
    lat2 = float(flask.request.args.get("lat2"))
    lng2 = float(flask.request.args.get("lng2"))
    points = int(flask.request.args.get("points"))

    coords, meters_per_pt = calculate_points(lat1, lng1, lat2, lng2, points)
    all_forecasts = retrieve_forecasts(coords, meters_per_pt)

    return_content = json.dumps(all_forecasts, cls=forecast.ForecastSerializer)
    logging.debug('responses: %s', return_content)
    return flask.Response(return_content, mimetype='application/json')

def calculate_points(lat1, lng1, lat2, lng2, points):
    ns_distance = great_circle((lat1, lng1), (lat2, lng1))
    ew_distance = great_circle((lat1, lng1), (lat1, lng2))
    area = ns_distance.meters * ew_distance.meters
    meters_per_pt = math.sqrt(area/points)
    km_per_pt = meters_per_pt/1000

    points_per_col = int(math.floor(ew_distance.meters/meters_per_pt))
    points_per_row = int(math.floor(ns_distance.meters/meters_per_pt))

    curr_pt = geopy.Point(lat1, lng1)
    coords = []
    for x in xrange(points_per_row + 1):
        row_start = curr_pt
        for x in xrange(points_per_col + 1):
            coords.append(Coordinates(curr_pt.latitude, curr_pt.longitude))
            curr_pt = move_point_east(curr_pt, lng2, km_per_pt)
        curr_pt = move_point_south(row_start, lat2, km_per_pt)

    return coords, meters_per_pt

def move_point_south(curr_pt, southern_lat, km):
    south_bearing = determine_bearing(math.radians(curr_pt.latitude),
                                      math.radians(curr_pt.longitude),
                                      math.radians(southern_lat),
                                      math.radians(curr_pt.longitude))
    return great_circle().destination(curr_pt, south_bearing, km)

def move_point_east(curr_pt, eastern_lng, km):
    east_bearing = determine_bearing(math.radians(curr_pt.latitude),
                                     math.radians(curr_pt.longitude),
                                     math.radians(curr_pt.latitude),
                                     math.radians(eastern_lng))
    return great_circle().destination(curr_pt, east_bearing, km)

def determine_bearing(lat1, lon1, lat2, lon2):
    dLon = lon2 - lon1
    y = math.sin(dLon) * math.cos(lat2)
    x = math.cos(lat1)*math.sin(lat2) - math.sin(lat1)*math.cos(lat2)*math.cos(dLon)
    brng = math.degrees(math.atan2(y, x))
    return brng


def retrieve_forecasts(coords, resolution):
    cached_forecasts = []
    missing_forecasts = []
    for coord in coords:
        cached_forecast = cache_repo.find(coord, (resolution)*.95)
        if cached_forecast:
            cached_forecast.coordinates = coord
            cached_forecasts.append(cached_forecast)
        else:
            missing_forecasts.append(coord)

    logging.info('missing coords: %s', len(missing_forecasts))
    logging.info('cached coords: %s', len(cached_forecasts))

    if missing_forecasts:
        new_forecast_dwml = noaa_proxy.request_dwml_grid_points(missing_forecasts)
        logging.debug('dwml new forecasts: %s', new_forecast_dwml)
        parser = DWML_Parser(new_forecast_dwml)
        new_forecasts = parser.generate_forecast_grid()
        logging.debug('new forecasts: %s', new_forecasts)
        for new_forecast in new_forecasts:
            cache_repo.insert(new_forecast)
    else:
        new_forecasts = []

    return new_forecasts + cached_forecasts


def start_server():
    port = int(os.environ.get('PORT', 5000))
    app.debug = True
    app.run(host='0.0.0.0', port=port)



if __name__ == "__main__":
    start_server()

