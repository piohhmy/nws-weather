from nws import mongo_cache
from nws import weather_hunter
from nws.forecast import Coordinates

def main():
    mongo_cache.empty()
    # Portland area
    lat1=36.672531
    lng1=-116.503419
    lat2=40.231227
    lng2=-113.942380
    
    points=150
    coords, distance_per_pt = weather_hunter.calculate_points(lat1, lng1, lat2, lng2, points)
    all_forecasts = weather_hunter.retrieve_forecasts(coords, distance_per_pt)

if __name__ == '__main__':
    main()