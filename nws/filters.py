import datetime

def sun_in_forecast(forecast):
    return bool([weather for weather in forecast.daily_weather.values() \
                 if condition_is_sunny(weather.condition)])

def condition_is_sunny(condition):
    return any(["Sunny" in condition, "Mostly Cloudy" in condition, "Partly Cloudy" in condition])

def sun_in_forecast_on_date(forecast, date):
    if date.isoformat() in forecast.daily_weather:
        return condition_is_sunny(forecast.daily_weather[date.isoformat()].condition)
    else:
        return False


def filter_by_sun(forecast_list):
    return [forecast for forecast in forecast_list if sun_in_forecast(forecast)]


def filter_by_sun_on_date(forecast_list, date):
    return [forecast for forecast in forecast_list if sun_in_forecast_on_date(forecast, date)]


