import flask
from nws import noaa_proxy
from nws.dwml_parser import DWML_Parser
from nws import dwml_parser
from nws import forecast
from nws import filters
from nws import mongo_cache as cache_repo
import json
import os
import datetime
import math
import logging

app = flask.Flask(__name__)

logging.basicConfig(filename='weatherhunter.log', level=logging.DEBUG)

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

    length = miles_between(lat1, lng1, lat2, lng2)
    width = miles_between(lat1, lng1, lat2, lng2)
    required_resolution = length * width / points

    dwml_coords = noaa_proxy.request_latlong_list(lat1, lng1, lat2, lng2, required_resolution)
    coords = dwml_parser.latlonlist_transform(dwml_coords)

    logging.info('coords: %s', coords)

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
    logging.info('dwml new forecasts: %s', new_forecast_dwml)
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

def miles_between(lat1, long1, lat2, long2):
    earth_radius_miles = 3960
    return distance_on_unit_sphere(float(lat1), float(long1), float(lat2), float(long2))  * earth_radius_miles


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

if __name__ == "__main__":
    start_server()

