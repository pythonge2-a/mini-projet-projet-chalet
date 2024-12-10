# lecture du fichier d'input 
import pandas as pd

file_path = 'data/simulated_weather_data.csv'
df = pd.read_csv(file_path)

last_row = df.tail(1)
#print(last_row)

current_date_time = last_row['datetime']
current_temperature = last_row['temperature']
current_luminosity = last_row['luminosity']
current_weather_condition = last_row['weather_condition']


def get_current_date_time():
    return current_date_time
def get_current_temperature():
    return current_temperature
def get_current_luminosity():
    return current_luminosity

# meteo condition --> 0: sunny, 1: cloudy, 2: rainy, 3: snowy, -1 error
def get_current_weather_condition():
    if current_weather_condition == 'sunny':
        return 0
    elif current_weather_condition == 'cloudy':
        return 1
    elif current_weather_condition == 'rainy':
        return 2
    elif current_weather_condition == 'snowy':
        return 3
    else:
        return -1

