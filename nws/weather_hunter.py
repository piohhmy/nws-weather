import flask
from nws import noaa_proxy
from nws.dwml_parser import DWML_Parser
from nws import dwml_parser
from nws import forecast
from nws.forecast import Coordinates
from nws import filters
from nws import mongo_cache as cache_repo
import json
import os
import datetime
import logging
import math

app = flask.Flask(__name__)

logging.basicConfig(filename='weatherhunter.log', level=logging.INFO)

@app.route("/weatherhunter/v1/gridlist")
def grid_list():
    lat = float(flask.request.args.get("lat"))
    lng = float(flask.request.args.get("lng"))
    distance = int(flask.request.args.get("distance"))
    resolution = flask.request.args.get("resolution")
    if resolution:
        resolution = int(resolution)
    else:
        resolution = 50
    dwml = noaa_proxy.request_dwml_grid(lat, lng, distance, distance, resolution)
    parser = DWML_Parser(dwml)
    forecast_grid = parser.generate_forecast_grid()
    return_content = json.dumps(forecast_grid, cls=forecast.ForecastSerializer)
    return flask.Response(return_content, mimetype='application/json')

@app.route("/weatherhunter/v2/gridlist")
def grid_list2():

    lat1 = float(flask.request.args.get("lat1"))
    lng1 = float(flask.request.args.get("lng1"))
    lat2 = float(flask.request.args.get("lat2"))
    lng2 = float(flask.request.args.get("lng2"))
    points = int(flask.request.args.get("points"))

    nwCoord = Coordinates(lat1,lng1)
    seCoord = Coordinates(lat2, lng2)
    neCoord = Coordinates(lat1, lng2)
    swCoord = Coordinates(lat2, lng1)

    length = nwCoord.miles_from(swCoord)
    logging.info('miles from nw pt to sw pt: %s', length)
    width = nwCoord.miles_from(neCoord)
    logging.info('miles from nw pt to ne pt: %s', width)
    area = length * width
    required_resolution = width/math.sqrt(points*width/length)
    logging.info('required resolution: %s', required_resolution)

    resolution = 5
    while True:
        dwml_coords = noaa_proxy.request_latlong_list(lat1, lng1, lat2, lng2, resolution)
        coords = dwml_parser.latlonlist_transform(dwml_coords)
        resolution = math.ceil(resolution * 1.5)
        if len(coords) < 200:
            break

    logging.info('num of coords: %s', len(coords))

    cached_forecasts = []
    missing_forecasts = []
    for coord in coords:
        cached_forecast = cache_repo.find(coord, required_resolution/2)
        if cached_forecast:
            cached_forecasts.append(cached_forecast)
        else:
            missing_forecasts.append(coord)

    logging.info('missing coords: %s', missing_forecasts)
    logging.info('cached coords: %s', cached_forecasts)

    new_forecast_dwml = noaa_proxy.request_dwml_grid_points(missing_forecasts)
    logging.debug('dwml new forecasts: %s', new_forecast_dwml)
    parser = DWML_Parser(new_forecast_dwml)
    new_forecasts = parser.generate_forecast_grid()
    logging.info('new forecasts: %s', new_forecasts)
    for new_forecast in new_forecasts:
        cache_repo.insert(new_forecast)

    all_forecasts = new_forecasts + cached_forecasts
    return_content = json.dumps(all_forecasts, cls=forecast.ForecastSerializer)

    return flask.Response(return_content, mimetype='application/json')

@app.route("/weatherhunter/v1/sun")
def sun():
    lat = float(flask.request.args.get("lat"))
    lng = float(flask.request.args.get("lng"))
    distance = int(flask.request.args.get("distance"))
    days_from_today = flask.request.args.get("days_from_today")
    resolution = flask.request.args.get("resolution")
    if resolution:
        resolution = int(resolution)
    else:
        resolution = 50

    dwml = noaa_proxy.request_dwml_grid(lat, lng, distance, distance, resolution)
    parser = DWML_Parser(dwml)
    forecast_grid = parser.generate_forecast_grid()
    if days_from_today:
        days_from_today = int(days_from_today)
        requested_date = datetime.date.today() + datetime.timedelta(days=days_from_today)
        sun_filtered_forecast = filters.filter_by_sun_on_date(forecast_grid, requested_date)
    else:
        sun_filtered_forecast = filters.filter_by_sun(forecast_grid)

    return_content = json.dumps(sun_filtered_forecast, cls=forecast.ForecastSerializer)
    return flask.Response(return_content, mimetype='application/json')

def start_server():
    port = int(os.environ.get('PORT', 5000))
    app.debug = True
    app.run(host='0.0.0.0', port=port)



if __name__ == "__main__":
    start_server()

