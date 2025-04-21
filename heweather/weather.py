import requests
from urllib.parse import urljoin

from .config import config
from .model import AirApi, DailyApi, HourlyApi, NowApi, WarningApi
from .errors import APIError, CityNotFoundError, ConfigError
from .utils import get_jwt_token


class Weather:

    def __init__(self, city_name: str, api_type: int = 0):
        self.city_name = city_name
        self.api_type = api_type
        self.host = config.qweather_apihost

        self._forecast_days()

        self.city_id = None
        self.now = None
        self.daily = None
        self.air = None
        self.warning = None
        self.hourly = None

        self.__reference = "\n请参考: https://dev.qweather.com/docs/start/status-code/"

    def _forecast_days(self):
        self.forecast_days = config.qweather_forecase_days
        if self.forecast_days:
            if self.api_type == 0 and not (3 <= self.forecast_days <= 7):
                raise ConfigError("api_type = 0 免费订阅 预报天数必须 3<= x <=7")

    def load_data(self):
        self.city_id = self._get_city_id()
        self.now = self._now()
        self.daily = self._daily()
        self.air = self._air()
        self.warning = self._warning()
        self.hourly = self._hourly()
        self._data_validate()

    def _get_data(self, url, params: dict) -> dict:
        headers = {
            "Authorization": f"Bearer {get_jwt_token()}",
        }

        res = requests.get(url, params=params, headers=headers)
        return res.json()

    def _get_city_id(self):
        url = urljoin(self.host, "/geo/v2/city/lookup")
        res = self._get_data(
            url=url,
            params={"location": self.city_name, "number": 1},
        )

        if res["code"] == "404":
            raise CityNotFoundError()
        elif res["code"] != "200":
            raise APIError("错误! 错误代码: {}".format(res["code"]) + self.__reference)
        else:
            self.city_name = res["location"][0]["name"]
            return res["location"][0]["id"]

    def _data_validate(self):
        if self.now.code == "200" and self.daily.code == "200":
            pass
        else:
            raise APIError(
                "错误! 请检查配置! "
                f"错误代码: now: {self.now.code}  "
                f"daily: {self.daily.code}  "
                + "air: {}  ".format(self.air.code if self.air else "None")
                + "warning: {}".format(self.warning.code if self.warning else "None")
                + self.__reference
            )

    def _check_response(self, response: dict) -> bool:
        if response.get('code') == "200":
            return True
        else:
            raise APIError(f"Response code:{response.get('code')}")

    def _now(self) -> NowApi:
        url = urljoin(self.host, "/v7/weather/now")
        res = self._get_data(
            url=url,
            params={"location": self.city_id},
        )
        self._check_response(res)
        return NowApi(**res)

    def _daily(self) -> DailyApi:
        url = urljoin(self.host, f"/v7/weather/{self.forecast_days}d")
        res = self._get_data(
            url=url,
            params={"location": self.city_id},
        )
        self._check_response(res)
        return DailyApi(**res)

    def _air(self) -> AirApi:
        url = urljoin(self.host, "/v7/air/now")
        res = self._get_data(
            url=url,
            params={"location": self.city_id},
        )
        self._check_response(res)
        return AirApi(**res)

    def _warning(self):
        url = urljoin(self.host, "/v7/warning/now")
        res = self._get_data(
            url=url,
            params={"location": self.city_id},
        )
        self._check_response(res)
        return None if res.get("code") == "204" else WarningApi(**res)

    def _hourly(self) -> HourlyApi:
        url = urljoin(self.host, "/v7/weather/24h")
        res = self._get_data(
            url=url,
            params={"location": self.city_id},
        )
        self._check_response(res)
        return HourlyApi(**res)