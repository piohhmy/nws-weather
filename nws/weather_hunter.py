import flask
from nws import noaa_proxy
from nws.dwml_parser import DWML_Parser
from nws import forecast
from nws import filters
import json
import os
import datetime

app = flask.Flask(__name__)

@app.route("/weatherhunter/v1/gridlist")
def grid_list():
    lat = float(flask.request.args.get("lat"))
    lng = float(flask.request.args.get("lng"))
    distance = int(flask.request.args.get("distance"))

    dwml = noaa_proxy.request_dwml_grid(lat, lng, distance, distance)
    parser = DWML_Parser(dwml)
    forecast_grid = parser.generate_forecast_grid()
    return_content = json.dumps(forecast_grid, cls=forecast.ForecastSerializer)
    return flask.Response(return_content, mimetype='application/json')

@app.route("/weatherhunter/v1/sun")
def sun():
    lat = float(flask.request.args.get("lat"))
    lng = float(flask.request.args.get("lng"))
    distance = int(flask.request.args.get("distance"))
    days_from_today = flask.request.args.get("distance")
        
    dwml = noaa_proxy.request_dwml_grid(lat, lng, distance, distance)
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

