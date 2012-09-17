import bottle
from nws import noaa_proxy
from nws.dwml_parser import DWML_Parser
from nws import forecast
import json
app = bottle.Bottle()

@app.route("/weatherhunter/gridlist.svc")
def grid_list():
    lat = float(bottle.request.query.lat)
    lng = float(bottle.request.query.lng)
    distance = int(bottle.request.query.distance)

    dwml = noaa_proxy.request_dwml_grid(lat, lng, distance, distance)
    parser = DWML_Parser(dwml)
    forecast_grid = parser.generate_forecast_grid()
    return json.dumps(forecast_grid, cls=forecast.ForecastSerializer)

def start_server():
    bottle.run(app, host='localhost', port=8080)

if __name__ == "__main__":
    start_server()
    
