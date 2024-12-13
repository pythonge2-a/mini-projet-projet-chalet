# lecture du fichier d'input 
import pandas as pd
import matplotlib.pyplot as plt

file_path = 'data/simulated_weather_data.csv'
df = pd.read_csv(file_path)

last_row = df.tail(1)
last_row = last_row.to_dict(orient='records')[0]

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
    if current_weather_condition == 'Sunny':
        return 0
    elif current_weather_condition == 'Cloudy':
        return 1
    elif current_weather_condition == 'Rainy':
        return 2
    elif current_weather_condition == 'Snowy':
        return 3
    else:
        return -1
    
# graphs
def get_temperature_graph():
    return df['temperature'].tolist()
def get_luminosity_graph():
    return df['luminosity'].tolist()
def get_weather_condition_graph():
    return df['weather_condition'].tolist()


def show_temperature_graph():
    plt.plot(get_temperature_graph())
    plt.title('Temperature')
    plt.show()
def show_luminosity_graph():
    plt.plot(get_luminosity_graph())
    plt.title('Luminosity')
    plt.show()
def show_weather_condition_graph():
    #afficher des points et non des lignes
    plt.plot(get_weather_condition_graph(), 'o')
    plt.title('Weather Condition')
    plt.show()

def show_all_graphs():
    ## 3 sur meme graph
    fig, axs = plt.subplots(3)
    fig.suptitle('Weather Data')
    axs[0].plot(get_temperature_graph())
    axs[0].set_title('Temperature')
    axs[1].plot(get_luminosity_graph())
    axs[1].set_title('Luminosity')
    axs[2].plot(get_weather_condition_graph(),'o')
    axs[2].set_title('Weather Condition')
    plt.show()

show_all_graphs()




