# Dans mqtt_client.py

import paho.mqtt.client as mqtt
import time

MQTT_BROKER = '192.168.4.1'
MQTT_PORT = 1883
MQTT_TOPIC_PUB = 'pico/leds/control'

# Dictionnaire pour stocker les dernières valeurs reçues par topic
mqtt_values = {}
connected_clients = set()

client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected with result code "+str(rc))
        # Subscribe to topics
        client.subscribe("capteur/#")
        print("Subscribed to capteur/#")
        # Add client to connected clients
        client_id = client._client_id.decode()
        connected_clients.add(client_id)
        print_connected_clients()
    else:
        print("Bad connection Returned code=", rc)

def on_message(client, userdata, msg):
    try:
        value = msg.payload.decode()
        mqtt_values[msg.topic] = value
        print(f"Received {msg.topic}: {value}")
    except Exception as e:
        print(f"Error processing message: {e}")

def on_client_disconnect(client, userdata, rc):
    client_id = client._client_id.decode()
    if client_id in connected_clients:
        connected_clients.remove(client_id)
    print_connected_clients()

def print_connected_clients():
    """Affiche la liste des clients connectés de manière formatée"""
    print("\n=== Connected MQTT Clients ===")
    if connected_clients:
        for client_id in connected_clients:
            print(f"- {client_id}")
    else:
        print("No clients connected")
    print("===========================\n")

client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_client_disconnect

def connect():
    try:
        print(f"Connecting to MQTT broker: {MQTT_BROKER}:{MQTT_PORT}")
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_start()

        time.sleep(2)

        if not client.is_connected():
            raise Exception("Failed to connect to MQTT broker")
        print("Connected to MQTT broker")
    except Exception as e:
        print(f"MQTT Connection error: {e}")

def publish_message(message):
    try:
        print(f"Publishing message: {message}")
        result = client.publish(MQTT_TOPIC_PUB, message)
        status = result[0]
        if status == 0:
            print("Message published successfully.")
        else:
            print("Failed to publish message.")
    except Exception as e:
        print(f"Error: {e}")

def get_value(mqtt_topic):
    try:
        value = mqtt_values.get(mqtt_topic)
        if value is not None:
            try:
                return float(value)
            except ValueError:
                return value
        return None
    except ValueError:
        return value
    except Exception as e:
        print(f"Error getting value from topic {mqtt_topic}: {e}")
        return None

def get_connected_clients():
    return list(connected_clients)

def close_connection():
    publish_message("intLed/OFF")
    publish_message("led1/OFF")
    client.loop_stop()
    client.disconnect()
    print("Disconnected from MQTT broker")