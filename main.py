import os

from heweather.weather import Weather
from heweather.render import render, html_to_image
from heweather.config import config


weather = Weather(config.qweather_city, config.qweather_api_type)
weather.load_data()
html = render(weather)

with open('weather.html', 'w') as f:
    f.write(html)

os.system("mkdir -p publish/ && cp -r heweather/templates/* publish/ && mv weather.html publish/")
html_to_image('publish/weather.html', 'publish/weather.png')
os.system("rm publish/weather.html")
