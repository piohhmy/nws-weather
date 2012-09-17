import flask
from nws import noaa_proxy
from nws.dwml_parser import DWML_Parser
from nws import forecast
import json
import os
app = flask.Flask(__name__)

@app.route("/weatherhunter/gridlist.svc")
def grid_list():
    lat = float(flask.request.args.get("lat"))
    lng = float(flask.request.args.get("lng"))
    distance = int(flask.request.args.get("distance"))

    dwml = noaa_proxy.request_dwml_grid(lat, lng, distance, distance)
    parser = DWML_Parser(dwml)
    forecast_grid = parser.generate_forecast_grid()
    return_content = json.dumps(forecast_grid, cls=forecast.ForecastSerializer) 
    return flask.Response(return_content, mimetype='application/json')

def start_server():
    port = int(os.environ.get('PORT', 5000))
    app.debug = True
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    start_server()
    
