# Process des data et les rend disponibles pour l'application
#

import reading as rd

#
# Récupère les données actuelles avec reading
#

def get_current_date_time():
    return rd.get_current_date_time()

def get_current_temperature():
    return rd.get_current_temperature()

def get_current_luminosity():
    return rd.get_current_luminosity()

def light_on():
    if (get_current_luminosity() < 100):
        return True
    else:
        return False
