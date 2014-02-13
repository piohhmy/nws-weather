from nws import weather_hunter
from nws.forecast import Coordinates

def main():
    # Portland area
    cached_areas = [
       {'lat1':44.185485, 'lng1':-123.942186, 'lat2':46.875841, 'lng2':-121.381148},
       {'lat1':46.270669, 'lng1':-124.762519, 'lat2':48.507950, 'lng2':-122.201480},
       {'lat1':46.306617, 'lng1':-123.221894, 'lat2':48.542403, 'lng2':-120.660856},
       {'lat1':46.137396, 'lng1':-120.310942, 'lat2':48.380212, 'lng2':-117.749904},
       {'lat1':46.306617, 'lng1':-123.221894, 'lat2':48.542403, 'lng2':-120.660856},
       {'lat1':45.421914, 'lng1':-124.314005, 'lat2':47.694247, 'lng2':-121.752967},
       {'lat1':36.672531, 'lng1':-116.503419, 'lat2':40.231227, 'lng2':-113.942380},
       {'lat1':36.672531, 'lng1':-116.503419, 'lat2':40.231227, 'lng2':-113.942380},
       {'lat1':36.672531, 'lng1':-116.503419, 'lat2':40.231227, 'lng2':-113.942380},
       {'lat1':42.564048, 'lng1':-122.771674, 'lat2':44.950919, 'lng2':-120.210635}
       ]


    points=150
    for area in cached_areas:
        coords, distance_per_pt = weather_hunter.calculate_points(points=points, **area)
        all_forecasts = weather_hunter.retrieve_forecasts(coords, distance_per_pt)

if __name__ == '__main__':
    main()
