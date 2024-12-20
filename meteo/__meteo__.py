import requests
import time

# Remplacez par votre clé API et les coordonnées
API_KEY = "a6c1dbb02550e86bcd5e14e948c3bba3"
LATITUDE = 46.77920475844563
LONGITUDE = 6.6589111250491975
BASE_URL_current = "https://api.openweathermap.org/data/2.5/weather"
 
# Construire l'URL de la requête
params = {
    "limit": 500,
    "sort": "desc",
    "lat": LATITUDE,
    "lon": LONGITUDE,
    "appid": API_KEY,
    "units": "metric",  # Température en Celsius
    "lang": "fr"        # Description météo en français
    
}
 
# Effectuer la requête
response = requests.get(BASE_URL_current, params=params)
 
if response.status_code == 200:
    data = response.json()
    # Extraire des données utiles
    print(data)
    
    temperature = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    description = data["weather"][0]["description"]
    city = data["name"]  # Nom de la ville correspondante    
else:
    print(f"Erreur : Impossible de récupérer les données ({response.status_code}).")








# graph de la région ### vent pluie température humitité pression 
URL_historic = "http://api.openweathermap.org/data/2.5/onecall/timemachine"

# Fonction pour récupérer les données météo historiques
def fetch_weather_for_day(API_KEY, lat, lon, timestamp):
    params = {
        "lat": lat,
        "lon": lon,
        "dt": timestamp,
        "appid": API_KEY,
        "units": "metric", 
    }
    response = requests.get(URL_historic, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erreur {response.status_code}: {response.text}")
        return None

# Collecter les données pour les 5 derniers jours
historical_data = []
current_time = int(time.time())  # Temps actuel en UNIX
for day in range(5):  # Jusqu'à 5 jourst
    timestamp = current_time - (day * 86400)  # Un jour = 86400 secondes
    day_data = fetch_weather_for_day(API_KEY, LATITUDE, LONGITUDE, timestamp)
    if day_data and "hourly" in day_data:
        historical_data.extend(day_data["hourly"])

# Afficher les données
print(f"Nombre de données collectées : {len(historical_data)}")
print(historical_data)


