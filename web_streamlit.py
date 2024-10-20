import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import time
from db_handler import calculate_and_store_daily_summary


def get_weather_data_from_db():
    conn = sqlite3.connect('weather.db')
    query = "SELECT city, date, temp, weather_condition, timestamp FROM weather_data ORDER BY timestamp DESC"
    data = pd.read_sql_query(query, conn)
    conn.close()
    return data

st.title("Real-Time Weather Monitoring")

daily_summary = calculate_and_store_daily_summary()

if daily_summary.empty:
    st.write("No daily summary data available.")
else:
    st.write("Daily Weather Summary")
    st.dataframe(daily_summary)

    cities = daily_summary['city'].unique()

    for city in cities:
        city_data = daily_summary[daily_summary['city'] == city]
        
        dominant_condition = city_data['dominant_condition'].iloc[0]
        st.write(f"Dominant Weather Condition for {city}: {dominant_condition}")

        fig, ax = plt.subplots(figsize=(10, 5))
        
        bar_width = 0.25
        x = range(len(city_data['date']))
        
        ax.bar(x, city_data['avg_temp'], width=bar_width, label='Avg Temp', color='lightblue')

        ax.bar([p + bar_width for p in x], city_data['max_temp'], width=bar_width, label='Max Temp', color='red')

        ax.bar([p + bar_width * 2 for p in x], city_data['min_temp'], width=bar_width, label='Min Temp', color='blue')

        ax.set_xticks([p + bar_width for p in x])
        ax.set_xticklabels(city_data['date'], rotation=45)

        ax.set_xlabel('Date')
        ax.set_ylabel('Temperature (°C)')
        ax.set_title(f'Temperature Trends for {city}')
        ax.legend()

        st.pyplot(fig)
        if city_data['max_temp'].max() > 30:
            st.warning("High temperature alert! Stay hydrated.")


    time.sleep(60)
    st.rerun()
