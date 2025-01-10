# Process des data et les rend disponibles pour l'application
#

import sim as sim

#
# Récupère les données actuelles avec reading
#

def get_current_date_time():
    return sim.get_current_date_time()

def get_current_temperature():
    return sim.get_current_temperature()

def get_current_luminosity():
    return sim.get_current_luminosity()

def get_state_lamp():
    return sim.get_current_lamp_state()

#
# Automation, logique
#

def light_on():
    for i in get_state_lamp():
        if (get_current_luminosity() < 100):    # 100 lux
            return True
        else:
            return False
        
def heating_on_living_room():
    if get_current_temperature() < 21:  # 21°C
        return True
    else:
        return False
    
def heating_on_bedroom():
    if get_current_temperature() < 18:  # 18°C
        return True
    else:
        return False
    
def velux_open():
    if get_current_temperature() > 20 and get_current_luminosity() > 100:   # 20°C et 100 lux
        return True
    else:
        return False
    
def store_open():
    if get_current_temperature() > 20 and get_current_luminosity() > 100:   # 20°C et 100 lux
        return True
    else:
        return False




