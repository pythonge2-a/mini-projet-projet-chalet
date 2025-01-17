#
# Process des data et les rend disponibles pour l'application
#

import database as db

#
# Récupère les données actuelles avec reading
#

def get_current_date_time():
    return db.get_current_date_time()

def get_current_temperature():
    return db.get_current_temperature()

def get_current_luminosity():
    return db.get_current_luminosity()

def get_state_lamp():
    return db.get_current_lamp_state()

#
# Automation, logique
#

def light_on_bedroom():
    for i in get_state_lamp():
        if (get_current_luminosity() < 100):    # 100 lux
            db.update_device_state('lamp_bedroom', 'on')
        else:
            db.update_device_state('lamp_bedroom', 'off')
        
def heating_on_living_room():
    if get_current_temperature() < 21:  # 21°C
        db.update_device_state('heater_rest_of_chalet', 'on')
    else:
        db.update_device_state('heater_rest_of_chalet', 'off')
    
def heating_on_bedroom():
    if get_current_temperature() < 18:  # 18°C
        db.update_device_state('heater_bedroom', 'on')
    else:
        db.update_device_state('heater_bedroom', 'off')
    
def velux_open():
    if get_current_temperature() > 20 and get_current_luminosity() > 100:   # 20°C et 100 lux
        db.update_device_state('velux_living_room', 'open')
    else:
        db.update_device_state('velux_living_room', 'closed')
    
def store_open():
    if get_current_temperature() > 20 and get_current_luminosity() > 100:   # 20°C et 100 lux
        db.update_device_state('store_living_room', 'open')
    else:
        




