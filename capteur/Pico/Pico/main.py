import time
import machine
import network
from umqtt.simple import MQTTClient

# Configuration for the built-in LED (GPIO 2 for the Pico WH)
intLed = machine.Pin("LED", machine.Pin.OUT)  # Use "LED" for Pico WH
led1 = machine.PWM(12)  # Use GPIO 12 for Pico
led1.freq(1000)  # Set PWM frequency to 1 kHz

# Wi-Fi configuration
SSID = "RaspberryAP"
PASSWORD = "TintinBinlin"

# MQTT Broker details
BROKER = "192.168.4.1"  # Replace with the Raspberry Pi's IP address
TOPIC = "pico/leds/control"  # Topic to control the LEDs

# Connect to Wi-Fi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to Wi-Fi...")
        wlan.connect(SSID, PASSWORD)
        while not wlan.isconnected():
            time.sleep(1)
            print("Waiting for connection...")
    print("Connected to Wi-Fi!")
    print("Network config:", wlan.ifconfig())

# Callback function when a message is received
def sub_cb(topic, msg):
    print(f"Message received on {topic}: {msg}")
    if msg == b"intLed/ON":
        intLed.value(1)  # Turn the LED ON
    elif msg == b"intLed/OFF":
        intLed.value(0)  # Turn the LED OFF
    elif msg == b"led1/OFF":
        led1.duty_u16(0)
    elif msg.startswith(b"led1/"):
        duty = int(msg.split(b"/")[1]) * 65535 // 100
        led1.duty_u16(duty)

# Connect to the MQTT broker
def connect_mqtt():
    client = MQTTClient("pico", BROKER)
    client.set_callback(sub_cb)
    client.connect()
    print("Connected to MQTT broker")
    client.subscribe(TOPIC)
    return client

# Main loop
def main():
    connect_wifi()  # First, connect to Wi-Fi
    client = connect_mqtt()  # Then connect to the MQTT broker

    try:
        while True:
            client.check_msg()  # Check for MQTT messages
            time.sleep(0.1)  # Small delay to save CPU
    except KeyboardInterrupt:
        print("Disconnecting...")
        client.disconnect()

# Run the main program
main()