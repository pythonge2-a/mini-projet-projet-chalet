#
# Process des data et les rend disponibles pour l'application
#
import database as db
import schedule
import threading
import time

def light_on_living_room():
    if db.get_device_state('lamp_living_room_switch'):    
        db.update_device_state('lamp_living_room', 'on')
    else:
        db.update_device_state('lamp_living_room', 'off')
        
def light_on_bedroom():
    if db.get_device_state('lamp_bedroom_switch'):    
        db.update_device_state('lamp_bedroom', 'on')
    else:
        db.update_device_state('lamp_bedroom', 'off')
        
def light_on_kitchen():
    if db.get_device_state('lamp_kitchen_switch'):    
        db.update_device_state('lamp_kitchen', 'on')
    else:
        db.update_device_state('lamp_kitchen', 'off')
        
def light_on_bathroom():
    if db.get_device_state('lamp_bathroom_switch'):    
        db.update_device_state('lamp_bathroom', 'on')
    else:
        db.update_device_state('lamp_bathroom', 'off')
        
def heating_on_living_room():
    if db.get_device_state('temperature sensor_rest_of_chalet') < 21:  # 21°C
        db.update_device_state('heater_rest_of_chalet', 'on')
    else:
        db.update_device_state('heater_rest_of_chalet', 'off')
    
def heating_on_bedroom():
    if db.get_device_state('temperature sensor_bedroom') < 18:  # 18°C
        db.update_device_state('heater_bedroom', 'on')
    else:
        db.update_device_state('heater_bedroom', 'off')
    
def velux_open():
    if db.get_device_state('humidity sensor_all') > 20 and db.get_device_state('luminosity_living_room') > 100:   # 20°C et 100 lux
        db.update_device_state('skylight_living_room', 'open')
    else:
        db.update_device_state('skylight_living_room', 'closed')
    
def store_open():
    if db.get_device_state('temperature sensor_rest_of_chalet') > 20 and db.get_device_state('luminosity_living_room') > 100:   # 20°C et 100 lux
        db.update_device_state('store_living_room', 'open')
    else:
        db.update_device_state('store_living_room', 'closed')
        

def update_data():
    light_on_living_room()
    light_on_bedroom()
    light_on_kitchen()
    light_on_bathroom()
    heating_on_living_room()
    heating_on_bedroom()
    velux_open()
    store_open()
    
    print("Data updated successfully")

schedule.every(1).seconds.do(update_data)

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

thread = threading.Thread(target=run_scheduler, daemon=True)
thread.start()



