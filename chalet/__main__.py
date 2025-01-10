from chalet.meteo.meteo import start_scheduler as mt_start_scheduler
from . import database as db
from chalet.mqtt_client import print_connected_clients, publish_message
import os
import sys
from pathlib import Path
import click 
from .database import DB_FILE
import threading

sys.path.append(str(Path(__file__).resolve().parent))

from chalet.manage import main as manage_main

@click.group()
def main():
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

    file_path = './chalet/database/data.db'
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"{file_path} has been deleted")
    else:
        print(f"{file_path} does not exist, so new one created")
    seed()
    pass

@main.command()
def seed():
    database = db.Database(DB_FILE)
    if database.connection is not None:
        database.create_tables()
        database.insert_data()
        database.close_connection()
    else:
        print("Failed to create the database connection")
    start_meteo_scheduler()
    runserver()
    pass

def start_meteo_scheduler():
    print("Starting the meteo scheduler thread")
    meteo_scheduler_thread = threading.Thread(target=mt_start_scheduler)
    meteo_scheduler_thread.daemon = True
    meteo_scheduler_thread.start()

@main.command()
@click.argument('ip', default='0.0.0.0:8000')
def runserver(ip):
    manage_main('runserver', ip)

if __name__ == "__main__":
    main()