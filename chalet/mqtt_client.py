import paho.mqtt.client as mqtt
import time

MQTT_BROKER = '192.168.4.1'
MQTT_PORT = 1883
MQTT_TOPIC_PUB = 'pico/leds/control'

received_message = None

client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected with result code "+str(rc))
    else:
        print("Bad connection Returned code=", rc)

client.on_connect = on_connect

def connect():
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_start()
    except Exception as e:
        print(f"Error: {e}")

def publish_message(message):
    try:
        print(f"Publishing message: {message}")
        result = client.publish(MQTT_TOPIC_PUB, message)
        status = result[0]
        if status == 0:
            print(f"Message published successfully.")
        else:
            print(f"Failed to publish message.")
    except Exception as e:
        print(f"Error: {e}")

def on_message(client, userdata, msg):
    global received_message
    received_message = msg.payload.decode()
    print(f"Received message: {received_message}")

client.on_message = on_message

def subscribe_and_get_message(mqtt_topic):
    global received_message
    received_message = None
    
    try:
        client.subscribe(mqtt_topic)
        # Wait up to 5 seconds for message
        timeout = 5
        start_time = time.time()
        while received_message is None and time.time() - start_time < timeout:
            time.sleep(0.1)
        return received_message
    except Exception as e:
        print(f"Error subscribing: {e}")
        return None
    
def get_value(mqtt_topic):
    try:
        value = subscribe_and_get_message(mqtt_topic)
        if value is not None:
            return float(value)  # Convertit en float si c'est une valeur numérique
        return None
    except ValueError:
        # Si la conversion en float échoue, retourne la valeur brute
        return value
    except Exception as e:
        print(f"Error getting value from topic {mqtt_topic}: {e}")
        return None