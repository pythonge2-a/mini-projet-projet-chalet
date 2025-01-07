import requests
import time
import json
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import os

API_KEY = "a6c1dbb02550e86bcd5e14e948c3bba3"
LATITUDE = 46.77920475844563
LONGITUDE = 6.6589111250491975
HISTORICAL_FILE = "historical_weather_data.json"  # Nom du fichier pour stocker les données
GRAPH_FOLDER = "meteo/graphs"  # Dossier pour les graphiques
file_path = os.path.join(GRAPH_FOLDER, "simple_graph.png")

# Fonction pour charger l'historique à partir du fichier JSON
def load_history():
    try:
        with open(HISTORICAL_FILE, "r") as file:
            history = json.load(file)
            return history
    except FileNotFoundError:
        # Si le fichier n'existe pas encore, retourner un dictionnaire vide
        return {}

# Fonction pour sauvegarder les données historiques dans un fichier JSON
def save_history(data):
    with open(HISTORICAL_FILE, "w") as file:
        json.dump(data, file, indent=4)


def get_weather_data(history):
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={LATITUDE}&lon={LONGITUDE}&appid={API_KEY}&units=metric"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        
        temperature = data['main']['temp']
        pressure = data['main']['pressure']
        humidity = data['main']['humidity']
        weather_description = data['weather'][0]['description']
        timestamp = time.time()  # Obtenir le timestamp actuel
        
        # Obtenir la date actuelle pour associer les données à un jour spécifique
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        # Ajouter les nouvelles données dans l'historique pour cette date
        if current_date not in history:
            history[current_date] = {
                "temperatures": [],
                "pressures": [],
                "humidities": [],
                "weather_conditions": [],
                "timestamps": []
            }
        
        history[current_date]["temperatures"].append(temperature)
        history[current_date]["pressures"].append(pressure)
        history[current_date]["humidities"].append(humidity)
        history[current_date]["weather_conditions"].append(weather_description)
        history[current_date]["timestamps"].append(timestamp)
        
        seven_days_ago = datetime.now() - timedelta(days=7)
        date_limit = seven_days_ago.strftime("%Y-%m-%d")
        
        
        history = {day: data for day, data in history.items() if day >= date_limit}
        
        save_history(history)
        
    else:
        print("Erreur lors de la récupération des données météo.")

def plot_weather_data(history):
    all_temperatures = []
    all_pressures = []
    all_humidities = []
    all_weather_conditions = []  # Liste pour stocker les conditions météo
    all_dates = []

    # Rassembler toutes les données pour tous les jours
    for date, data in history.items():
        for i, temp in enumerate(data["temperatures"]):
           
            if i == 0:
                all_dates.append(date)
            else:
                all_dates.append("")  

            all_temperatures.append(temp)
            all_pressures.append(data["pressures"][i])
            all_humidities.append(data["humidities"][i])
            all_weather_conditions.append(data["weather_conditions"][i])

    # Assurez-vous que le dossier existe avant de sauvegarder l'image
    if not os.path.exists(GRAPH_FOLDER):
        os.makedirs(GRAPH_FOLDER)

    fig, axs = plt.subplots(4, 1, figsize=(10, 16), sharex=True)

    # Graphique de la température
    axs[0].plot(all_temperatures, label="Température", linestyle='-', marker='o', color='tab:blue')
    axs[0].set_title("Évolution de la Température")
    axs[0].set_ylabel("Température (°C)")
    axs[0].grid(True)
    axs[0].legend()

    # Graphique de la pression
    axs[1].plot(all_pressures, label="Pression", linestyle='-', marker='o', color='tab:orange')
    axs[1].set_title("Évolution de la Pression")
    axs[1].set_ylabel("Pression (hPa)")
    axs[1].grid(True)
    axs[1].legend()

    # Graphique de l'humidité
    axs[2].plot(all_humidities, label="Humidité", linestyle='-', marker='o', color='tab:green')
    axs[2].set_title("Évolution de l'Humidité")
    axs[2].set_ylabel("Humidité (%)")
    axs[2].grid(True)
    axs[2].legend()

    # Graphique des conditions météo
    weather_labels = list(set(all_weather_conditions))  # Liste des conditions météo uniques
    
    weather_colors = {
        'clear sky': '#FFDD00',   # Jaune clair
        'few clouds': '#A9A9A9',   # Gris clair
        'scattered clouds': '#A9A9A9',  # Gris clair
        'broken clouds': '#A9A9A9',  # Gris
        'shower rain': '#00CED1',  # Cyan
        'rain': '#1E90FF',         # Bleu
        'thunderstorm': '#8A2BE2', # Violet
        'snow': '#FFFFFF',         # Blanc
        'mist': '#98FB98'          # Vert pâle
    }
    
    weather_color_map = [weather_colors.get(condition, '#808080') for condition in all_weather_conditions]

    # Scatter plot des conditions météo
    scatter = axs[3].scatter(range(len(all_weather_conditions)), [0] * len(all_weather_conditions), c=weather_color_map, s=50, marker='o', edgecolors='none')
    axs[3].set_title("Conditions Météorologiques")
    axs[3].set_yticks([])  # On ne veut pas d'échelle sur l'axe Y
    axs[3].set_xlabel("Mesures")
    axs[3].grid(False)

    # Ajouter les dates sur l'axe X pour la première mesure de chaque jour
    axs[3].set_xticks(range(len(all_temperatures)))
    axs[3].set_xticklabels(all_dates, rotation=45)

    # Ajuster l'axe X pour que les dates n'apparaissent qu'une seule fois par jour
    axs[3].tick_params(axis='x', which='major', labelsize=10)  
    axs[3].set_xticks([i for i in range(len(all_temperatures)) if all_dates[i] != ""])  
    axs[3].set_xticklabels([d for d in all_dates if d != ""])  

    # Ajouter la légende des couleurs
    handles = []
    for condition, color in weather_colors.items():
        handles.append(plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=10, label=condition))

    axs[3].legend(handles=handles, title="Conditions Météo", bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)

    # Sauvegarder le graphique
    plt.tight_layout()
    plt.savefig(file_path)


while 0: # a mettre a 1 
    history = load_history()
    get_weather_data(history)
    plot_weather_data(history)
    
    time.sleep(900)  # Pause de 15 minutes avant la mise à jour suivante
