from nose.tools import *
from nws import mongo_cache as cache_repo
class TestMongoCache():
	def test_find_with_no_match(self):
		coord = (124.2,23.12) 
		resolution = 34
		result = cache_repo.find(coord, resolution)
		assert_equal(result, None)

	