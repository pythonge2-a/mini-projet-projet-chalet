from chalet.meteo.meteo import start_scheduler as mt_start_scheduler
from chalet.process_data.process import start_scheduler as pd_start_scheduler
from chalet.database import Database as db, DB_FILE
from chalet.mqtt_client import connect as mqtt_connect, close_connection as mqtt_close_connection, print_connected_clients, publish_message
from chalet.manage import django_command
import os
import sys
from pathlib import Path
import click 
import threading
import signal
from typing import Any

sys.path.append(str(Path(__file__).resolve().parent))

meteo_scheduler_thread = None
process_scheduler_thread = None
database_instance = None

def signal_handler(signum: Any, frame: Any) -> None:
    """Handle clean shutdown when CTRL+C is pressed"""
    # Check if this is the main process or a Django reloader
    if os.environ.get('RUN_MAIN') != 'true':
        # Only handle signal in the main process
        # Prevent multiple executions
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        signal.signal(signal.SIGTERM, signal.SIG_IGN)

        print("\nExiting the application")
        global meteo_scheduler_thread, process_scheduler_thread, database_instance

        if database_instance is not None:
            database_instance.close_connection()

        mqtt_close_connection()

        if meteo_scheduler_thread is not None:
            meteo_scheduler_thread.join(timeout=1.0)
        if process_scheduler_thread is not None:
            process_scheduler_thread.join(timeout=1.0)

        print("Shutdown complete")
        sys.exit(0)

@click.group()
def main():
    signal.signal(signal.SIGINT, signal_handler)

@main.command()
def list_devices():
    mqtt_connect()
    print_connected_clients()

@main.command()
@click.argument('message')
def publish_mqtt(message):
    mqtt_connect()
    publish_message(message)

@main.command()
@click.pass_context
def cleandb(ctx):
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        print(f"{DB_FILE} has been deleted")
    else:
        print(f"{DB_FILE} does not exist, so new one created")
    ctx.invoke(seed)

@main.command()
def seed():
    global database_instance
    if not os.path.exists(DB_FILE):
        database_instance = db(DB_FILE)
        if database_instance.connection is not None:
            database_instance.create_tables()
            database_instance.insert_data()
            database_instance.close_connection()
        else:
            print("Failed to create the database connection")
    else:
        print(f"{DB_FILE} already exists")

def start_meteo_scheduler():
    print("Starting the meteo scheduler thread")
    meteo_scheduler_thread = threading.Thread(target=mt_start_scheduler)
    meteo_scheduler_thread.daemon = True
    meteo_scheduler_thread.start()

def start_process_data_scheduler():
    print("Starting the process data scheduler thread")
    process_scheduler_thread = threading.Thread(target=pd_start_scheduler)
    process_scheduler_thread.daemon = True
    process_scheduler_thread.start()

@main.command()
@click.argument('ip', default='0.0.0.0:8000')
@click.pass_context
def runserver(ctx, ip):
    ctx.invoke(seed)
    mqtt_connect()
    start_meteo_scheduler()
    start_process_data_scheduler()
    django_command('runserver', ip)

if __name__ == "__main__":
    main()