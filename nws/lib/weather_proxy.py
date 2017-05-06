import requests

def get_forecast_for(lat, lng):
    base = 'https://api.weather.gov/'
    resource = 'points/{},{}/forecast'.format(_clean(lat), _clean(lng))
    headers = {'user-agent': 'http://weatherhunt.com/'}
    r = requests.get(base+resource, headers=headers)
    r.raise_for_status()
    return r.json()

def _clean(coord):
    return round(float(coord), 4)
