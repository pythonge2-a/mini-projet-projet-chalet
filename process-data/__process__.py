# Process des data et les rend disponibles pour l'application
#

import reading as rd

#
# Récupère la date et l'heure actuelle
#
def get_current_date_time():
    return rd.get_current_date_time()

def get_current_temperature():
    return rd.get_current_temperature()

def get_current_luminosity():
    return rd.get_current_luminosity()

def get_current_weather_condition():
    return rd.get_current_weather_condition()

def light_on():
    if (get_current_luminosity() < 100 or get_current_weather_condition() == 2 or get_current_weather_condition() == 3):
        return True
    else:
        return False
