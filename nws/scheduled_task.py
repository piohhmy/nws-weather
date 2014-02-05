from nws.mongo_cache import MongoRepo
from nws import weather_hunter
from nws.forecast import Coordinates

def main():
    MongoRepo.empty()
    # Portland area
    lat1=44.185485
    lng1=-123.942186
    lat2=46.875841
    lng2=-121.381148
    
    points=150
    coords, distance_per_pt = weather_hunter.calculate_points(lat1, lng1, lat2, lng2, points)
    all_forecasts = weather_hunter.retrieve_forecasts(coords, distance_per_pt)

if __name__ == '__main__':
    main()