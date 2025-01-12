import paho.mqtt.client as mqtt

MQTT_BROKER = '192.168.4.1'
MQTT_PORT = 1883
MQTT_TOPIC = 'pico/leds/control'

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
        result = client.publish(MQTT_TOPIC, message)
        status = result[0]
        if status == 0:
            print(f"Message published successfully.")
        else:
            print(f"Failed to publish message.")
    except Exception as e:
        print(f"Error: {e}")