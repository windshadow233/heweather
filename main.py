from heweather.weather import Weather
from heweather.render import render
from heweather.config import config


weather = Weather(config.qweather_city, config.qweather_api_type)
weather.load_data()
html = render(weather)

with open('weather.html', 'w') as f:
    f.write(html)
