#include <DHT.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// Configuration du WiFi
const char* ssid = "RaspberryAP";
const char* password = "TintinBinlin";

// Configuration MQTT
const char* mqtt_server = "192.168.4.1";
const int mqtt_port = 1883;
const char* mqtt_user = "d1Mini";
const char* mqtt_password = "tintin";
const char* mqtt_topic_temp = "capteur/temperature";
const char* mqtt_topic_hum = "capteur/humidite";

// Définition de la broche où est connecté le DHT22
#define DHTPIN D3     // Connecter le DHT22 sur la broche D3 du D1 Mini
#define DHTTYPE DHT22 // DHT22 (AM2302)

// Initialisation du capteur DHT
DHT dht(DHTPIN, DHTTYPE);

// Instances pour WiFi et MQTT
WiFiClient espClient;
PubSubClient client(espClient);

// Variables pour les mesures
float temperature;
float humidite;
unsigned long dernierEnvoi = 0;
const long intervalleEnvoi = 10000;  // Intervalle d'envoi (10 secondes)

void setup_wifi() {
  delay(10);
  Serial.println("Connexion au WiFi...");
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nConnecté au WiFi");
  Serial.println("Adresse IP: ");
  Serial.println(WiFi.localIP());
}

void reconnect() {
  while (!client.connected()) {
    Serial.println("Connexion au broker MQTT...");
    String clientId = "D1MiniClient-";
    clientId += String(random(0xffff), HEX);

    if (client.connect(clientId.c_str(), mqtt_user, mqtt_password)) {
      Serial.println("Connecté au broker MQTT");
    } else {
      Serial.print("Échec de connexion, rc=");
      Serial.print(client.state());
      Serial.println(" nouvelle tentative dans 5 secondes");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  Serial.println("Initialisation...");
  delay(2000); // Attendre 2 secondes pour permettre au capteur de démarrer correctement
  setup_wifi();
  client.setServer(mqtt_server, mqtt_port);
  dht.begin();
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  unsigned long maintenant = millis();
  if (maintenant - dernierEnvoi >= intervalleEnvoi) {
    dernierEnvoi = maintenant;

    // Lecture des données du DHT22
    temperature = dht.readTemperature();
    humidite = dht.readHumidity();

    // Vérification si la lecture est valide
    if (isnan(temperature) || isnan(humidite)) {
      Serial.println("Erreur de lecture du DHT22!");
      client.publish(mqtt_topic_temp, "Erreur de lecture du DHT22!");
      client.publish(mqtt_topic_hum, "Erreur de lecture du DHT22!");
      return;
    }

    // Conversion des valeurs en chaînes
    char tempString[8];
    char humString[8];
    dtostrf(temperature, 1, 2, tempString);
    dtostrf(humidite, 1, 2, humString);

    // Publication des données
    client.publish(mqtt_topic_temp, tempString);
    client.publish(mqtt_topic_hum, humString);

    // Affichage sur le moniteur série
    Serial.print("Température: ");
    Serial.print(temperature);
    Serial.print("°C, Humidité: ");
    Serial.print(humidite);
    Serial.println("%");
  }
}