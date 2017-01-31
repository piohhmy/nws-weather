from lib.forecast import Forecast, Weather, Coordinates
from lib import filters
import datetime
from nose.tools import assert_equals

class TestSunFilter():
    def test_sunny_forecast_is_kept(self):
        sun_forecast = Forecast(Coordinates(127.13, 23.53))

        sun_weather = Weather(70, 40, "Sunny")
        sun_forecast.daily_weather[datetime.date.today()] = sun_weather

        rain_forecast = Forecast(Coordinates(123.13, 24.53))
        rain_weather = Weather(70, 40, "Rain")
        rain_forecast.daily_weather[datetime.date.today()] = rain_weather

        filtered_forecasts = filters.filter_by_sun([sun_forecast, rain_forecast])
        assert sun_forecast in filtered_forecasts
        assert rain_forecast not in filtered_forecasts

    def test_filter_with_multiple_dates(self):
        sun_weather = Weather(70, 40, "Sunny")
        rain_weather = Weather(70, 40, "Rain")

        forecast = Forecast(Coordinates(127.13, 23.53))
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)
        forecast.daily_weather[today.isoformat()] = rain_weather
        forecast.daily_weather[tomorrow.isoformat()] = sun_weather

        filtered_forecasts = filters.filter_by_sun([forecast])
        assert forecast in filtered_forecasts

    def test_filter_on_specific_date(self):
        sun_weather = Weather(70, 40, "Sunny")
        rain_weather = Weather(70, 40, "Rain")

        forecast = Forecast(Coordinates(127.13, 23.53))
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)
        forecast.daily_weather[today.isoformat()] = rain_weather
        forecast.daily_weather[tomorrow.isoformat()] = sun_weather

        filtered_forecasts = filters.filter_by_sun_on_date([forecast], today)
        assert forecast not in filtered_forecasts


    def test_filter_with_partly_sunny(self):
        sun_weather = Weather(70, 40, "Partly Sunny")
        rain_weather = Weather(70, 40, "Rain")

        forecast = Forecast(Coordinates(127.13, 23.53))
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)
        forecast.daily_weather[today.isoformat()] = rain_weather
        forecast.daily_weather[tomorrow.isoformat()] = sun_weather

        filtered_forecasts = filters.filter_by_sun([forecast])
        assert forecast in filtered_forecasts

    def test_filter_with_partly_cloudy(self):
        sun_weather = Weather(70, 40, "Partly Cloudy")
        cloud_weather = Weather(70, 40, "Cloudy")

        forecast = Forecast(Coordinates(127.13, 23.53))
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)
        forecast.daily_weather[today.isoformat()] = cloud_weather
        forecast.daily_weather[tomorrow.isoformat()] = sun_weather

        filtered_forecasts = filters.filter_by_sun([forecast])
        assert forecast in filtered_forecasts


    def test_cloudy_forecast_is_not_kept(self):
        cloud_forecast = Forecast(Coordinates(127.13, 23.53))

        cloud_weather = Weather(70, 40, "Cloudy")
        cloud_forecast.daily_weather[datetime.date.today()] = cloud_weather

        filtered_forecasts = filters.filter_by_sun([cloud_forecast])
        assert cloud_forecast not in filtered_forecasts

    def test_condition_is_sunny(self):
        assert not filters.condition_is_sunny("Rain")

    def test_filter_with_partly_sunny(self):
        sun_weather = Weather(70, 40, "Partly Sunny")
        cloud_weather = Weather(70, 40, "Mostly Cloudy")

        forecast = Forecast(Coordinates(127.13, 23.53))
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)
        forecast.daily_weather[today.isoformat()] = cloud_weather
        forecast.daily_weather[tomorrow.isoformat()] = sun_weather

        filtered_forecasts = filters.filter_by_sun_on_date([forecast], today)
        assert forecast in filtered_forecasts
        assert_equals (forecast.daily_weather[tomorrow.isoformat()].condition, "Partly Sunny")
