import os
from .model import HourlyType


class Config:
    qweather_city = os.environ.get('CITY_NAME')
    qweather_api_type = 0
    qweather_apihost = os.getenv('API_HOST')
    qweather_forecase_days = 7
    qweather_hourlytype = HourlyType.current_24h

    qweather_jwt_sub: str = os.getenv('JWT_SUB')
    qweather_jwt_private_key: str = os.getenv('PRIVATE_KEY')

    qweather_jwt_kid: str = os.getenv("JWT_KEY_ID")


config = Config()
