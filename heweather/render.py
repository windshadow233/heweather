from datetime import datetime
from pathlib import Path
import platform
from jinja2 import Environment, FileSystemLoader
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import time
from .config import config
from .model import Air, Daily, Hourly, HourlyType
from .weather import Weather


def render(weather: Weather) -> str:
    template_path = str(Path(__file__).parent / "templates")

    air = None
    if weather.air:
        if weather.air.now:
            air = add_tag_color(weather.air.now)

    templates = {
        "now": weather.now.now,
        "days": add_date(weather.daily.daily),
        "city": weather.city_name,
        "warning": weather.warning,
        "air": air,
        "hours": add_hour_data(weather.hourly.hourly),
    }
    env = Environment(loader=FileSystemLoader(template_path))
    template = env.get_template("index.html")
    return template.render(**templates)


def html_to_image(html_path, output_image='weather.png'):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)

    html_file_url = "file://" + os.path.abspath(html_path)
    driver.get(html_file_url)

    time.sleep(1)

    driver.set_window_size(1000, driver.execute_script("return document.body.scrollHeight") + 150)

    driver.get_screenshot_as_file(output_image)
    driver.quit()


def add_hour_data(hourly: list[Hourly]):
    min_temp = min([int(hour.temp) for hour in hourly])
    high = max([int(hour.temp) for hour in hourly])
    low = int(min_temp - (high - min_temp))
    for hour in hourly:
        date_time = datetime.fromisoformat(hour.fxTime)
        if platform.system() == "Windows":
            hour.hour = date_time.strftime("%#I%p")
        else:
            hour.hour = date_time.strftime("%-I%p")
        if high == low:
            hour.temp_percent = "100px"
        else:
            hour.temp_percent = f"{int((int(hour.temp) - low) / (high - low) * 100)}px"
    if config.qweather_hourlytype == HourlyType.current_12h:
        hourly = hourly[:12]
    if config.qweather_hourlytype == HourlyType.current_24h:
        hourly = hourly[::2]
    return hourly


def add_date(daily: list[Daily]):
    week_map = [
        "周日",
        "周一",
        "周二",
        "周三",
        "周四",
        "周五",
        "周六",
    ]

    for day in daily:
        date = day.fxDate.split("-")
        _year = int(date[0])
        _month = int(date[1])
        _day = int(date[2])
        week = int(datetime(_year, _month, _day, 0, 0).strftime("%w"))
        day.week = week_map[week] if day != 0 else "今日"
        day.date = f"{_month}月{_day}日"

    return daily


def add_tag_color(air: Air):
    color = {
        "优": "#95B359",
        "良": "#A9A538",
        "轻度污染": "#E0991D",
        "中度污染": "#D96161",
        "重度污染": "#A257D0",
        "严重污染": "#D94371",
    }
    air.tag_color = color[air.category]
    return air
