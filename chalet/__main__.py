from meteo import __meteo__ as mt
from . import database as db
from chalet.mqtt_client import print_connected_clients, publish_message
import os
import sys
from pathlib import Path
import click 
from .database import DB_FILE

sys.path.append(str(Path(__file__).resolve().parent))

from chalet.manage import main as manage_main

@click.group()
def main(command):
    pass 

@main.command()
def list_devices():
    print_connected_clients()

@main.command()
@click.argument('message')
def publish_mqtt(message):
    publish_message(message)

@main.command()
def cleandb():
    db.clear_database()
    pass

@main.command()
def seed():
    pass

@main.command()
@click.argument('ip', default='0.0.0.0:8000')
def runserver(ip):
    manage_main('runserver', ip)

if __name__ == "__main__":
    main()