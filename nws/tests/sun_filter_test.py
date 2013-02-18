from nws.forecast import Forecast, Weather, Coordinates
from nws import filters
import datetime

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
        assert rain_weather not in filtered_forecasts

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
