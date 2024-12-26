import requests
import time
import json
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

API_KEY = "a6c1dbb02550e86bcd5e14e948c3bba3"
LATITUDE = 46.77920475844563
LONGITUDE = 6.6589111250491975
HISTORICAL_FILE = "historical_weather_data.json"  # Nom du fichier pour stocker les données

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

# Fonction pour récupérer les données actuelles et les ajouter à l'historique
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
        
        # Supprimer les jours qui sont plus vieux que 7 jours
        history = {day: data for day, data in history.items() if day >= date_limit}
        
        # Sauvegarder les données mises à jour
        save_history(history)
        
    else:
        print("Erreur lors de la récupération des données météo.")

# Fonction pour générer un graphique des températures mises bout à bout
def plot_combined_temperatures(history):
    all_temperatures = []

    # Rassembler toutes les températures pour tous les jours
    for date, data in history.items():
        all_temperatures.extend(data["temperatures"])

    plt.figure(figsize=(12, 6))

    # Tracer toutes les températures combinées
    plt.plot(all_temperatures, label="Températures", linestyle='-', marker='o')

    plt.title("Températures sur les 7 Derniers Jours")
    plt.xlabel("Mesures toutes les 15 minutes")
    plt.ylabel("Température (°C)")
    plt.grid(True)
    plt.legend()
    
    # Affichage du graphique
    plt.tight_layout()
    plt.show()

# Fonction pour obtenir la dernière température
def get_last_temperature(history):
    last_temp = None
    for day, data in history.items():
        if isinstance(data, dict) and "temperatures" in data and data["temperatures"]:
            last_temp = data["temperatures"][-1]
    return last_temp

# Fonction pour obtenir la dernière pression
def get_last_pressure(history):
    last_pressure = None
    for day, data in history.items():
        if isinstance(data, dict) and "pressures" in data and data["pressures"]:
            last_pressure = data["pressures"][-1]
    return last_pressure

# Fonction pour obtenir la dernière humidité
def get_last_humidity(history):
    last_humidity = None
    for day, data in history.items():
        if isinstance(data, dict) and "humidities" in data and data["humidities"]:
            last_humidity = data["humidities"][-1]
    return last_humidity

# Fonction pour obtenir la dernière condition météo
def get_last_weather_condition(history):
    last_condition = None
    for day, data in history.items():
        if isinstance(data, dict) and "weather_conditions" in data and data["weather_conditions"]:
            last_condition = data["weather_conditions"][-1]
    return last_condition


history = load_history()
get_weather_data(history)

# Boucle pour récupérer les nouvelles données toutes les 15 minutes
while True:
    get_weather_data(history)

    # Après la récupération, afficher le graphique avec toutes les températures mises bout à bout
    plot_combined_temperatures(history)
    
    time.sleep(900)  # Attendre 15 minutes avant la prochaine récupération
