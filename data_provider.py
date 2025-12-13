import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry

LAT = 35.7139
LON = 51.4812
TIMEZONE = "Asia/Tehran"


def _client():
    cache = requests_cache.CachedSession(".cache", expire_after=3600)
    retry_session = retry(cache, retries=5, backoff_factor=0.2)
    return openmeteo_requests.Client(session=retry_session)


def get_weather_air_dataframe(hours=72) -> pd.DataFrame:
    client = _client()

    # ---------------- WEATHER ----------------
    weather_url = "https://api.open-meteo.com/v1/forecast"
    weather_params = {
        "latitude": LAT,
        "longitude": LON,
        "hourly": "weather_code",
        "timezone": TIMEZONE,
        "forecast_hours": hours,
    }

    w = client.weather_api(weather_url, params=weather_params)[0]
    wh = w.Hourly()

    times = pd.date_range(
        start=pd.to_datetime(wh.Time(), unit="s"),
        end=pd.to_datetime(wh.TimeEnd(), unit="s"),
        freq=pd.Timedelta(seconds=wh.Interval()),
        inclusive="left",
    )

    weather_df = pd.DataFrame({
        "time_iran": times,
        "weather_code": wh.Variables(0).ValuesAsNumpy(),
    })

    # ---------------- AIR QUALITY ----------------
    air_url = "https://air-quality-api.open-meteo.com/v1/air-quality"
    air_params = {
        "latitude": LAT,
        "longitude": LON,
        "hourly": [
            "pm10",
            "pm2_5",
            "carbon_monoxide",
            "nitrogen_dioxide",
            "ozone",
            "european_aqi",
        ],
        "timezone": TIMEZONE,
        "forecast_hours": hours,
    }

    a = client.weather_api(air_url, params=air_params)[0]
    ah = a.Hourly()

    air_df = pd.DataFrame({
        "time_iran": times,
        "pm10": ah.Variables(0).ValuesAsNumpy(),
        "pm2_5": ah.Variables(1).ValuesAsNumpy(),
        "co": ah.Variables(2).ValuesAsNumpy(),
        "no2": ah.Variables(3).ValuesAsNumpy(),
        "o3": ah.Variables(4).ValuesAsNumpy(),
        "aqi": ah.Variables(5).ValuesAsNumpy(),
    })

    return pd.merge(weather_df, air_df, on="time_iran")
