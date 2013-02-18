import datetime

def sun_in_forecast(forecast):
    return bool([weather for weather in forecast.daily_weather.values() if "Sunny" in weather.condition])

def sun_in_forecast_on_date(forecast, date):
    if date.isoformat() in forecast.daily_weather:
        return "Sunny" in forecast.daily_weather[date.isoformat()].condition
    else:
        return False


def filter_by_sun(forecast_list):
    return [forecast for forecast in forecast_list if sun_in_forecast(forecast)]


def filter_by_sun_on_date(forecast_list, date):
    print forecast_list[0].daily_weather
    return [forecast for forecast in forecast_list if sun_in_forecast_on_date(forecast, date)]


