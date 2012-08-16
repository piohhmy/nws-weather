import urllib2
import urllib
import xml.dom.minidom as minidom
import time
from forecast import *

def main():
    dwml = request_dwml_grid(45.5508, -122.738, 50.0, 50.0, 20.0)
    print dwml
    forecast_grid = parse_dwml(dwml)


def request_dwml_grid(lat, lng, lat_distance, lng_distance, resolution):
    noaaURL = "http://graphical.weather.gov/xml/sample_products/browser_interface/ndfdBrowserClientByDay.php"
    paramaters = {"centerPointLat" : lat, "centerPointLon" : lng, "distanceLat" : lat_distance, "distanceLon" : lng_distance, "resolutionSquare" : resolution, "numDays" : 7}
    url_query_string = urllib.urlencode(paramaters)
    url = noaaURL + "?" + url_query_string + "&format=24+hourly"
    #?centerPointLat=45.5508&centerPointLon=-122.738&distanceLat=50.0&distanceLon=50.0&resolutionSquare=20.0&format=24+hourly&numDays=7"
    f = urllib2.urlopen(url)
    print url
    dwml = f.read()
    return dwml

def parse_dwml(dwml):
    doc = minidom.parseString(dwml)
    locations = doc.getElementsByTagName("parameters")
    points = doc.getElementsByTagName("point")
    # TODO: Create objects from these

    forecast_grid = []

    for point in points:
        lat = point.getAttribute("latitude")
        lng = point.getAttribute("longitude")
        print "Latitude: " + lat
        print "Longitude: " + lng
        forecast = Forecast(Coordinates(lat, lng))
        forecast_grid.append(forecast)

    grid_index = 0
    for location in locations:
        temperatures = location.getElementsByTagName("temperature")
        for temp in temperatures:
            print temp.getAttribute('type')
            values = temp.getElementsByTagName("value")
            #TODO: populate Weather obj
            for value in values:
                if value.hasChildNodes() == True:
                    print value.firstChild.nodeValue
        conditions = location.getElementsByTagName("weather-conditions")
        for condition in conditions:
            print condition.getAttribute('weather-summary')

if __name__ == "__main__":
    main()
