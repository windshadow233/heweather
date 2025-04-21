import os

from heweather.weather import Weather
from heweather.render import render, html_to_image
from heweather.config import config


weather = Weather(config.qweather_city, config.qweather_api_type)
weather.load_data()
html = render(weather)

with open('index.html', 'w') as f:
    f.write(html)

os.system("mkdir -p publish/ && cp -r heweather/templates/* publish/ && mv index.html publish/")
html_to_image('publish/index.html', 'publish/weather.png')