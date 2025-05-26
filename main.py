import os
import asyncio

from heweather.weather import Weather
from heweather.render import render, html_to_image
from heweather.config import config


async def main():
    weather = Weather(config.qweather_city, config.qweather_api_type)
    await weather.load_data()
    html = render(weather)
    with open('heweather/templates/weather.html', 'w') as f:
        f.write(html)

    os.system("mkdir -p publish/ && cp heweather/templates/index.html publish/")
    await html_to_image('heweather/templates/weather.html', 'publish/weather.png')
    os.remove("heweather/templates/weather.html")


if __name__ == "__main__":
    asyncio.run(main())
    print("Weather data loaded and rendered successfully.")