# lecture du fichier d'input 
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

file_path = 'sim/data/chalet_data.csv'
df = pd.read_csv(file_path)

last_row = df.tail(1)
last_row = last_row.to_dict(orient='records')[0]

current_date_time = last_row['datetime']
current_temperature = last_row['temperature']
current_luminosity = last_row['luminosity']
current_humidity = last_row['humidity']
current_lamp1_state = last_row['lamp1']
current_lamp2_state = last_row['lamp2']
current_lamp3_state = last_row['lamp3']
current_velux_position = last_row['velux_pos']
def get_current_lamp_state():
    list_lamp = [current_lamp1_state, current_lamp2_state, current_lamp3_state]
    return list_lamp

def get_current_date_time():
    return current_date_time
def get_current_temperature():
    return current_temperature
def get_current_luminosity():
    return current_luminosity
def get_current_humidity():
    return current_humidity
def get_current_velux_position():
    return current_velux_position

# graphs
def get_temperature_graph():
    return df['temperature'].tolist()
def get_luminosity_graph():
    return df['luminosity'].tolist()
def get_humidity_graph():
    return df['humidity'].tolist()

def get_datetime_list():
    return df['datetime'].tolist()

def show_temperature_graph():
    plt.figure(figsize=(10, 5))
    plt.plot(get_datetime_list(), get_temperature_graph())
    plt.title('Temperature')
    plt.xlabel('Time')
    plt.ylabel('Temperature[°C]')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def show_luminosity_graph():
    plt.figure(figsize=(10, 5))
    plt.plot(get_datetime_list(), get_luminosity_graph())
    plt.title('Luminosity')
    plt.xlabel('Time')
    plt.ylabel('Luminosity[lux]')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def show_humidity_graph():
    plt.figure(figsize=(10, 5))
    plt.plot(get_datetime_list(), get_humidity_graph())
    plt.title('Humidity')
    plt.xlabel('Time')
    plt.ylabel('Humidity')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def show_all_graphs():
    fig, axs = plt.subplots(3, sharex=True, figsize=(10, 15))
    fig.suptitle('Weather Data[]')
    datetime_list = get_datetime_list()
    
    axs[0].plot(datetime_list, get_temperature_graph())
    axs[0].set_title('Temperature')
    axs[0].set_ylabel('Temperature[°C]')
    
    axs[1].plot(datetime_list, get_luminosity_graph())
    axs[1].set_title('Luminosity')
    axs[1].set_ylabel('Luminosity[lux]')
    
    axs[2].plot(datetime_list, get_humidity_graph())
    axs[2].set_title('Humidity')
    axs[2].set_ylabel('Humidity')
    axs[2].set_xlabel('Time')
    
    for ax in axs:
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        ax.tick_params(axis='x', rotation=45)
    
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()


# get meteo infos 




