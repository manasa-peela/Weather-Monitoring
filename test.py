from data_processing import kelvin_to_celsius, parse_weather_data, get_weather_data
from db_handler import store_weather_data, calculate_daily_summary
from config import CITY_IDS

import time

def run_tests():
    # Test data retrieval
    print("Testing data retrieval...")
    weather_data = get_weather_data(CITY_IDS['Delhi'])
    print("Data retrieval successful!\n")

    # Test temperature conversion
    print("Testing temperature conversion...")
    assert kelvin_to_celsius(273.15) == 0.0
    print("Temperature conversion successful!\n")

    # Test daily summary calculation
    print("Testing daily summary calculation...")
    test_weather = {'temp': 298.15, 'feels_like': 298.15, 'weather_condition': 'Clear', 'timestamp': time.time()}
    store_weather_data('Delhi', test_weather)
    summary = calculate_daily_summary('Delhi')
    print(f"Summary: {summary}")
    print("Daily summary calculation successful!\n")

    # Test alerting mechanism
   


# Run all tests
if __name__ == "__main__":
    run_tests()
