from enum import IntEnum

from pydantic import BaseModel


class Now(BaseModel):
    obsTime: str
    temp: str
    icon: str
    text: str
    windScale: str
    windDir: str
    humidity: str
    precip: str
    vis: str


class NowApi(BaseModel):
    code: str
    now: Now


class Daily(BaseModel):
    fxDate: str
    week: str = None
    date: str = None
    tempMax: str
    tempMin: str
    textDay: str
    textNight: str
    iconDay: str
    iconNight: str


class DailyApi(BaseModel):
    code: str
    daily: list[Daily]


class Air(BaseModel):
    category: str
    aqi: str
    pm2p5: str
    pm10: str
    o3: str
    co: str
    no2: str
    so2: str
    tag_color: str = None


class AirApi(BaseModel):
    code: str
    now: Air = None


class Warning(BaseModel):
    title: str
    type: str
    pubTime: str
    text: str


class WarningApi(BaseModel):
    code: str
    warning: list[Warning] = None


class Hourly(BaseModel):
    fxTime: str
    hour: str = None
    temp: str
    icon: str
    text: str
    temp_percent: str = None


class HourlyApi(BaseModel):
    code: str
    hourly: list[Hourly]


class HourlyType(IntEnum):
    current_12h = 1
    current_24h = 2