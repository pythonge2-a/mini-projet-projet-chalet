# Description: This file contains the DeviceService class 
# which is responsible for handling the light switches state changes 
# and updating the sensor data in the database.

from typing import Dict, Any
from chalet.mqtt_client import publish_message
import chalet.process_data.process as pd

class DeviceService:
    @staticmethod
    def handle_lights(request, db) -> None:
        """Handles light switches state changes"""
        switches = {
            'toggle_light_room': 'lamp_bedroom_switch',
            'toggle_light_living': 'lamp_living_room_switch',
            'toggle_light_kitchen': 'lamp_kitchen_switch',
            'toggle_light_bathroom': 'lamp_bathroom_switch'
        }
        
        for form_name, db_name in switches.items():
            if form_name in request.POST:
                new_state = 1 if request.POST.get(form_name) == 'on' else 0
                pd.write_data(db_name, new_state, db)
                if form_name == 'toggle_light_room':
                    publish_message('intLed/ON' if new_state == 1 else 'intLed/OFF')

    @staticmethod
    def update_sensors(room_data: Dict[str, Any], db) -> None:
        """Updates sensor data in the database"""
        pd.write_data("temperature sensor_bedroom", room_data['temperature'], db)
        pd.write_data("humidity sensor_all", room_data['humidity'], db)

    @staticmethod
    def build_context(db, weather_data, room_data):
        """Builds the context for the captors.html template"""
        return {
            'room_temperature_value': pd.get_data('temperature sensor_bedroom', db) if pd.get_data('temperature sensor_bedroom', db) != -1000 else 'N/A',
            'room_humidity_value': pd.get_data('humidity sensor_all', db) if pd.get_data('humidity sensor_all', db) != -1000 else 'N/A',
            'light_status_room': pd.get_data('lamp_bedroom_switch', db) == 1,
            'living_temperature_value': 22.5,
            'living_humidity_value': 50.0,
            'light_status_living': pd.get_data('lamp_living_room_switch', db) == 1,
            'kitchen_temperature_value': 22.5,
            'kitchen_humidity_value': 50.0,
            'light_status_kitchen': pd.get_data('lamp_kitchen_switch', db) == 1,
            'bathroom_temperature_value': 22.5,
            'bathroom_humidity_value': 50.0,
            'light_status_bathroom': pd.get_data('lamp_bathroom_switch', db) == 1,
            'outside_temperature_value': weather_data['temperature'],
            'outside_pressure_value': weather_data['pressure'],
            'outside_humidity_value': weather_data['humidity'],
            'outside_weather': weather_data['weather']
        }