import os

from heweather.weather import Weather
from heweather.render import render, html_to_image
from heweather.config import config


weather = Weather(config.qweather_city, config.qweather_api_type)
weather.load_data()
html = render(weather)

with open('heweather/templates/weather.html', 'w') as f:
    f.write(html)

os.system("mkdir -p publish/ && cp heweather/templates/index.html publish/")
html_to_image('heweather/templates/weather.html', 'publish/weather.png')
os.system("rm heweather/templates/weather.html")
