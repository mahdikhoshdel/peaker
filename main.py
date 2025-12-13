from data_provider import get_weather_air_dataframe
from interpreter import human_report
from pprint import pprint
import pandas as pd


import pandas as pd

def get_conditions_at(df, iran_time: str | None = None):
    """
    Returns the closest FUTURE forecast.
    If iran_time is None -> uses current Iran time.
    """

    if iran_time is None:
        t = pd.Timestamp.now(tz="Asia/Tehran").tz_localize(None)
    else:
        t = pd.Timestamp(iran_time)

    future = df[df["time_iran"] >= t]

    if not future.empty:
        return future.iloc[0]   # closest future hour

    # Fallback: last available forecast
    return df.iloc[-1]



if __name__ == "__main__":
    df = get_weather_air_dataframe()

    iran_time = "2025-12-13 18:30"
    row = get_conditions_at(df, iran_time)

    report = human_report(row)
    pprint(report)
