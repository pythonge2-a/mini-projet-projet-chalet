import paho.mqtt.client as mqtt

MQTT_BROKER = '192.168.4.1'
MQTT_PORT = 1883
MQTT_TOPIC = 'pico/leds/control'

client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

client.on_connect = on_connect

def connect():
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()

def publish_message(message):
    client.publish(MQTT_TOPIC, message)