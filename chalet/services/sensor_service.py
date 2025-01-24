# Description: Service to get the weather and room data

from typing import Dict, Any
from chalet.meteo.meteo import load_history, get_weather_data
from chalet.mqtt_client import get_value

class SensorService:
    @staticmethod
    def get_weather_data() -> Dict[str, Any]:
        """Gets the weather data"""
        try:
            history = load_history()
            temp, pressure, humidity, weather = get_weather_data(history, save=False)
            if None in (temp, pressure, humidity, weather):
                raise Exception('Error while getting weather data')
            return {
                'temperature': temp,
                'pressure': pressure,
                'humidity': humidity,
                'weather': weather
            }
        except Exception as e:
            print(f"Error getting weather data: {e}")
            return {
                'temperature': 'N/A',
                'pressure': 'N/A',
                'humidity': 'N/A',
                'weather': 'N/A'
            }
        
    @staticmethod
    def get_room_data() -> Dict[str, float]:
        """Gets the room data"""
        try:
            temp = get_value("capteur/temperature")
            humidity = get_value("capteur/humidite")
            if None in (temp, humidity):
                raise Exception('Error while getting room data')
            return {
                'temperature': temp,
                'humidity': humidity
            }
        except Exception as e:
            print(f"Error getting room data: {e}")
            return {
                'temperature': -1000,
                'humidity': -1000
            }