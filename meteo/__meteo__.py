import requests


# Remplacez par votre clé API et les coordonnées
API_KEY = "a6c1dbb02550e86bcd5e14e948c3bba3"
LATITUDE = 46.77920475844563
LONGITUDE = 6.6589111250491975
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
 
# Construire l'URL de la requête
params = {
    "lat": LATITUDE,
    "lon": LONGITUDE,
    "appid": API_KEY,
    "units": "metric",  # Température en Celsius
    "lang": "fr"        # Description météo en français
}
 
# Effectuer la requête
response = requests.get(BASE_URL, params=params)
 
if response.status_code == 200:
    data = response.json()
    # Extraire des données utiles
    temperature = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    description = data["weather"][0]["description"]
    city = data["name"]  # Nom de la ville correspondante
    print(f"La température actuelle à {city} (coordonnées: {LATITUDE}, {LONGITUDE}) est de {temperature}°C avec {description}.")
    print(f"L'humidité est de {humidity}%.")
else:
    print(f"Erreur : Impossible de récupérer les données ({response.status_code}).")