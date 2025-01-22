#
# Process des data et les rend disponibles pour l'application
#
from chalet.database import Database, DB_FILE
from chalet.mqtt_client import publish_message
import sched
import time

scheduler = sched.scheduler(time.time, time.sleep)

def get_db():
    return Database(DB_FILE)

def write_data(device_type, new_state, db=None):
    try:
        flag = False
        if db is None:
            flag = True
            db = get_db()
        db.update_device_state(device_type, new_state)
        if flag:
            db.close_connection()
    except Exception as e:
        print(f"Error writing data: {e}")

def get_data(device_type, db=None):
    try:
        flag = False
        if db is None:
            flag = True
            db = get_db()
        result = db.get_device_state(device_type)
        if flag:
            db.close_connection()
        return result
    except Exception as e:
        print(f"Error getting data: {e}")
        return None

def update_data():
    try:
        db = get_db()
        light_on_living_room(db)
        light_on_bedroom(db)
        light_on_kitchen(db)
        light_on_bathroom(db)
        heating_on_living_room(db)
        heating_on_bedroom(db)
        velux_open(db)
        store_open(db)
        print("Data updated successfully")
        db.close_connection()
    except Exception as e:
        print(f"Error updating data: {e}")

def light_on_living_room(db: Database) -> None:
    try:
        switch_state = db.get_device_state('lamp_living_room_switch')
        current_state = db.get_device_state('lamp_living_room')
        print(f"Switch state for living room: {switch_state}")
        if switch_state != current_state:    
            db.update_device_state('lamp_living_room', switch_state)
            print("Living room light turned", "ON" if switch_state == 1 else "OFF")
    except Exception as e:
        print(f"Error in light_on_living_room: {e}")
        
def light_on_bedroom(db: Database) -> None:
    try:
        switch_state = db.get_device_state('lamp_bedroom_switch')
        current_state = db.get_device_state('lamp_bedroom')
        print(f"Switch state for bedroom: {switch_state}")
        if switch_state != current_state:    
            db.update_device_state('lamp_bedroom', switch_state)
            print("Bedroom light turned", "ON" if switch_state == 1 else "OFF")
    except Exception as e:
        print(f"Error in light_on_bedroom: {e}")
        
def light_on_kitchen(db: Database) -> None:
    try:
        switch_state = db.get_device_state('lamp_kitchen_switch')
        current_state = db.get_device_state('lamp_kitchen')
        print(f"Switch state for kitchen: {switch_state}")
        if switch_state != current_state:    
            db.update_device_state('lamp_kitchen', switch_state)
            print("Kitchen light turned", "ON" if switch_state == 1 else "OFF")
    except Exception as e:
        print(f"Error in light_on_kitchen: {e}")
        
def light_on_bathroom(db: Database) -> None:
    try:
        switch_state = db.get_device_state('lamp_bathroom_switch')
        current_state = db.get_device_state('lamp_bathroom')
        print(f"Switch state for bathroom: {switch_state}")
        if switch_state != current_state:    
            db.update_device_state('lamp_bathroom', switch_state)
            print("Bathroom light turned", "ON" if switch_state == 1 else "OFF")
    except Exception as e:
        print(f"Error in light_on_bathroom: {e}")
        
def heating_on_living_room(db: Database) -> None:
    if db.get_device_state('temperature sensor_rest_of_chalet') < 21:  # 21°C
        db.update_device_state('heater_rest_of_chalet', 1)
    else:
        db.update_device_state('heater_rest_of_chalet', 0)
    
def heating_on_bedroom(db: Database) -> None:
    # This programme is weird because it's for a presentation 
    # the real version should work like that
    """if db.get_device_state('temperature sensor_bedroom') < 18:  # 18°C
        db.update_device_state('heater_bedroom', 1)
    else:
        db.update_device_state('heater_bedroom', 0)"""
    try:
        humidity = db.get_device_state('humidity sensor_all')
        print(f"Current humidity state: {humidity if humidity != -1000 else 'N/A'}")
        if humidity is not None and humidity != -1000:
            intensity = min(max(humidity, 0), 100) # Ensure that the value is between 0 and 100
            print(f"Setting heater intensity to {intensity}")
            publish_message(f"led1/{intensity}")
            db.update_device_state('heater_bedroom', intensity)
    except Exception as e:
        print(f"Error in heating_on_bedroom: {e}")
    
def velux_open(db: Database) -> None:
    if db.get_device_state('humidity sensor_all') > 20 and db.get_device_state('luminosity_living_room') > 100:   # 20°C et 100 lux
        db.update_device_state('skylight_living_room', 1)
    else:
        db.update_device_state('skylight_living_room', 0)
    
def store_open(db: Database) -> None:
    if db.get_device_state('temperature sensor_rest_of_chalet') > 20 and db.get_device_state('luminosity_living_room') > 100:   # 20°C et 100 lux
        db.update_device_state('store_living_room', 1)
    else:
        db.update_device_state('store_living_room', 0)

def scheduled_task():
    try:
        print("Running scheduled task...")
        update_data()  # Exécute update_data
        print("Update data task completed")
        scheduler.enter(5, 1, scheduled_task)
    except Exception as e:
        print(f"Error in scheduled task: {e}")
        # En cas d'erreur, réessayer après 10 secondes
        scheduler.enter(10, 1, scheduled_task)

def start_scheduler():
    scheduler.enter(0, 1, scheduled_task)
    scheduler.run()

