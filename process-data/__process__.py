# Process des data et les rend disponibles pour l'application
#

import sim as rd

#
# Récupère les données actuelles avec reading
#

def get_current_date_time():
    return rd.get_current_date_time()

def get_current_temperature():
    return rd.get_current_temperature()

def get_current_luminosity():
    return rd.get_current_luminosity()

def get_state_lamp():
    return rd.get_current_lamp_state()

def light_on():
    for i in get_state_lamp():
        if (get_current_luminosity() < 100):
            return True
        else:
            return False
        
def temperature_on():
    if get_current_temperature() > 25:
        return False
    else:
        return True

        


