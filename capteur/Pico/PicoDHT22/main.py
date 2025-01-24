"""import network
import time
from machine import Pin
import dht
from umqtt.simple import MQTTClient

# WiFi configuration
SSID = 'RaspberryAP'
PASSWORD = 'TintinBinlin'

# MQTT configuration
MQTT_BROKER = '192.168.4.1'
MQTT_TOPIC = 'pico/sensor'
MQTT_CLIENT_ID = 'pico_' + str(time.time())  # Unique ID pour éviter les conflits
MQTT_KEEPALIVE = 30

# DHT22 configuration
DHT_PIN = 28

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.config(pm = 0xa11140)  # Disable power-save mode
    
    if wlan.isconnected():
        wlan.disconnect()
    
    print("Connecting to Wi-Fi...")
    wlan.connect(SSID, PASSWORD)
    
    max_wait = 10
    while max_wait > 0:
        if wlan.isconnected():
            break
        max_wait -= 1
        print("Waiting for connection...")
        time.sleep(1)
    
    if wlan.isconnected():
        print("Connected to Wi-Fi!")
        print("Network config:", wlan.ifconfig())
        return True
    else:
        print("Connection failed!")
        return False

def read_dht22():
    sensor = dht.DHT22(Pin(DHT_PIN))
    retry_count = 3  # Nombre de tentatives de lecture
    
    for _ in range(retry_count):
        try:
            sensor.measure()
            temp = sensor.temperature()
            hum = sensor.humidity()
            
            # Vérification des valeurs aberrantes
            if -40 <= temp <= 80 and 0 <= hum <= 100:
                print(f'Temperature: {temp:.1f}°C, Humidity: {hum:.1f}%')
                return temp, hum
        except OSError as e:
            print(f"Retry sensor reading... ({e})")
            time.sleep(2)
    
    return None, None

def connect_mqtt():
    try:
        client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, keepalive=MQTT_KEEPALIVE)
        client.connect()
        print("Connected to MQTT broker")
        return client
    except Exception as e:
        print("MQTT connection failed:", e)
        return None

def publish_data(client, temp, hum):
    if temp is not None and hum is not None:
        try:
            payload = f'{{"temperature": {temp:.1f}, "humidity": {hum:.1f}}}'  # Format JSON
            client.publish(MQTT_TOPIC, payload.encode())
            print('Published:', payload)
            return True
        except Exception as e:
            print("Publish error:", e)
            return False
    else:
        try:
            payload = '{"error": "No valid sensor data"}'
            client.publish(MQTT_TOPIC, payload.encode())
            print("Published error message")
            return True
        except Exception as e:
            print("Publish error:", e)
            return False

def main():
    while True:
        if not connect_wifi():
            print("WiFi connection failed. Retrying in 10 seconds...")
            time.sleep(10)
            continue
            
        mqtt_client = connect_mqtt()
        if not mqtt_client:
            print("MQTT connection failed. Retrying in 10 seconds...")
            time.sleep(10)
            continue
        
        while True:
            try:
                temp, hum = read_dht22()
                if not publish_data(mqtt_client, temp, hum):
                    raise Exception("Failed to publish data")
                time.sleep(10)
                
            except Exception as e:
                print("Error in main loop:", e)
                break
        
        print("Reconnecting in 10 seconds...")
        time.sleep(10)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Program stopped by user")
    except Exception as e:
        print("Fatal error:", e)"""
from lib.dht_sensor import DHT22  # Remplacez par le bon chemin si nécessaire
from machine import Pin
import time

DHT_PIN = 28  # La broche GPIO utilisée pour le capteur
sensor = DHT22(DHT_PIN)  # Passez directement le numéro de broche

while True:
    try:
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        print(f'Temperature: {temp:.1f}°C, Humidity: {hum:.1f}%')
    except Exception as e:
        print("Error:", e)
    time.sleep(2)
