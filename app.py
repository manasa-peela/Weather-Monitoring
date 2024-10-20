from data_processing import get_weather_data, parse_weather_data
from db_handler import store_weather_data, calculate_daily_summary,calculate_and_store_daily_summary
from alerts import check_alerts
from config import CITY_IDS, INTERVAL
import sqlite3
import pandas as pd

import time

def main():
    while True:
        for city, city_id in CITY_IDS.items():
            weather_data_raw = get_weather_data(city_id)
            weather_data = parse_weather_data(weather_data_raw)
            weather_data = pd.DataFrame([weather_data])
            # store_weather_data(city, weather_data)
            conn = sqlite3.connect('weather.db')
            weather_data.to_sql('weather_data', conn, if_exists='append', index=False)
            conn.close()
            
            summary = calculate_and_store_daily_summary()
            check_alerts(weather_data)

            # Optionally, print daily summary
            # summary = calculate_daily_summary(city)
            if not summary.empty:
                print(f"Daily Summary for {city}: {summary}")

        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()
