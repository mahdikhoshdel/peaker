def weather_code_to_text(code: int) -> str:
    return {
        0: "Clear sky ☀️",
        1: "Mainly clear 🌤",
        2: "Partly cloudy ⛅",
        3: "Overcast ☁️",
        45: "Fog 🌫",
        61: "Rain 🌧",
        71: "Snow ❄️",
        95: "Thunderstorm ⛈",
    }.get(code, "Unknown weather")


def level(value, limits):
    for max_v, label in limits:
        if value <= max_v:
            return label
    return limits[-1][1]


def human_report(row) -> dict:
    return {
        "time": row["time_iran"].strftime("%Y-%m-%d %H:%M"),
        "weather": weather_code_to_text(int(row["weather_code"])),
        "air": {
            "AQI": f"{row['aqi']:.1f} ({level(row['aqi'], [(50,'Good'), (100,'Moderate'), (150,'Unhealthy')])})",
            "PM2.5": f"{row['pm2_5']} µg/m³ ({level(row['pm2_5'], [(12,'Good'), (35,'Moderate'), (55,'Unhealthy')])})",
            "PM10": f"{row['pm10']} µg/m³ ({level(row['pm10'], [(50,'Good'), (100,'Moderate')])})",
            "NO₂": f"{row['no2']} µg/m³ ({level(row['no2'], [(40,'Good'), (100,'Moderate')])})",
        },
        "advice": advice(row),
    }


def advice(row):
    if row["pm2_5"] > 35 or row["aqi"] > 100:
        return "Avoid outdoor activity. Sensitive groups stay indoors."
    if row["pm2_5"] > 25 or row["no2"] > 80:
        return "Limit long outdoor exercise, especially near traffic."
    return "Outdoor activities are safe."
