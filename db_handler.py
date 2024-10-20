import sqlite3
import time
import pandas as pd


conn = sqlite3.connect('weather.db')
c = conn.cursor()

# Create table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS weather_data (
                city TEXT,
                date TEXT,
                temp REAL,
                weather_condition TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
conn.commit()
conn.close()

def store_weather_data(city, weather_data):
    timestamp = weather_data['timestamp']
    date = time.strftime('%Y-%m-%d')
    temp = weather_data['temp']
    weather_condition = weather_data['weather_condition']

    c.execute("INSERT INTO weather_data (city, date, temp, weather_condition, timestamp) VALUES (?, ?, ?, ?, ?)",
              (city, date, temp, weather_condition, timestamp))
    conn.commit()
    conn.close()




def calculate_and_store_daily_summary():
    conn = sqlite3.connect('weather.db')
    
    query = "SELECT * FROM weather_data"
    data = pd.read_sql_query(query, conn)
    
    if data.empty:
        print("No data available for summary.")
        return

    daily_summary = data.groupby(['date','city']).agg(
        avg_temp=('temp', 'mean'),
        max_temp=('temp', 'max'),
        min_temp=('temp', 'min'),
        dominant_condition=('weather_condition', lambda x: x.mode()[0])  # Get most frequent weather condition
    ).reset_index()

    daily_summary.to_sql('daily_weather_summary', conn, if_exists='replace', index=False)

    conn.close()
    return daily_summary
