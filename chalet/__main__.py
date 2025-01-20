from meteo import __meteo__ as mt
from database import __database__ as db
from chalet.mqtt_client import print_connected_clients, publish_message
import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))

from chalet.manage import main as manage_main

def main():
    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "list_devices":
            print_connected_clients()
            return
        elif command == "publish_mqtt":
            if len(sys.argv) > 2:
                message = sys.argv[2]
                publish_message(message)
                return
            else:
                print("Error: No message provided")
                return
            
        args = sys.argv[2:]
    else:
        command = 'runserver'
        args = ['0.0.0.0:8000']

    manage_main(command, *args)

if __name__ == "__main__":
    main()