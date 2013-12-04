from nws import mongo_cache
from nws import weather_hunter
from nws.forecast import Coordinates

def main():
	mongo_cache.empty()
	coord1 = Coordinates(47.116020,-121.381148)
	coord2 = Coordinates(43.932427,-123.942186)
	#weather_hunter.hunt(coord1, coord2, 200)

if __name__ == '__main__':
	main()