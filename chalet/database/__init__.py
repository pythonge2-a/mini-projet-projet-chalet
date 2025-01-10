import sqlite3
from sqlite3 import Error
import os

class Database:
    def __init__(self, db_file):
        self.connection = self.create_connection(db_file)
    
    def create_connection(self, db_file):
        """Create a connection to the SQLite database specified by db_file."""
        connection = None
        try:
            connection = sqlite3.connect(db_file)
            print(f"Successfully connected to the database {db_file}")
        except Error as e:
            print(f"Error connecting to the database: {e}")
        return connection

    def create_tables(self):
        try:
            cursor = self.connection.cursor()
            # Create rooms table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS rooms (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL
                )
            ''')
            # Create devices table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS devices (
                    id INTEGER PRIMARY KEY,
                    type TEXT NOT NULL,
                    state TEXT NOT NULL
                )
            ''')
            # Create room_devices table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS room_devices (
                    room_id INTEGER NOT NULL,
                    device_id INTEGER NOT NULL,
                    FOREIGN KEY (room_id) REFERENCES rooms (id),
                    FOREIGN KEY (device_id) REFERENCES devices (id)
                )
            ''')
            # Create history table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS history (
                    id INTEGER PRIMARY KEY,
                    date TEXT NOT NULL,
                    temperature REAL,
                    pressure REAL,
                    humidity REAL,
                    weather_condition TEXT
                )
            ''')
            print("Tables created successfully")
        except Error as e:
            print(f"Error creating the tables: {e}")

    def insert_data(self):
        try:
            cursor = self.connection.cursor()
            # Insert rooms
            rooms = [
                ('bedroom',),
                ('bathroom',),
                ('living room',),
                ('kitchen',)
            ]
            cursor.executemany('INSERT INTO rooms (name) VALUES (?)', rooms)
            
            # Insert devices
            devices = [
                ('lamp_bedroom', 0),
                ('lamp_bathroom', 0),
                ('lamp_living_room', 0),
                ('lamp_kitchen', 0),
                ('heater_bedroom', 0),
                ('heater_rest_of_chalet', 0),
                ('skylight_living_room', 0),
                ('luminosity_living_room', 0),
                ('temperature sensor_bedroom', 0),
                ('temperature sensor_rest_of_chalet', 0),
                ('humidity sensor_all', 0),
                ('lamp_bedroom_switch',0),
                ('lamp_bathroom_switch', 0),
                ('lamp_living_room_switch', 0),
                ('lamp_kitchen_switch', 0),
            ]
            cursor.executemany('INSERT INTO devices (type, state) VALUES (?, ?)', devices)
            
            # Insert room_devices relationships
            room_devices = [
                (1, 1),  # bedroom -> lamp_bedroom
                (2, 2),  # bathroom -> lamp_bathroom
                (3, 3),  # living room -> lamp_living_room
                (4, 4),  # kitchen -> lamp_kitchen
                (1, 5),  # bedroom -> heater_bedroom
                (2, 6),  # bathroom -> heater_rest_of_chalet
                (3, 6),  # living room -> heater_rest_of_chalet
                (4, 6),  # kitchen -> heater_rest_of_chalet
                (3, 7),  # living room -> skylight
                (3, 8),  # living room -> luminosity_living_room
                (1, 9),  # bedroom -> temperature sensor_bedroom
                (2, 10), # bathroom -> temperature sensor_rest_of_chalet
                (3, 10), # living room -> temperature sensor_rest_of_chalet
                (4, 10), # kitchen -> temperature sensor_rest_of_chalet
                (1, 11), # bedroom -> humidity sensor_all
                (2, 11), # bathroom -> humidity sensor_all
                (3, 11), # living room -> humidity sensor_all
                (4, 11),  # kitchen -> humidity sensor_all
                (1, 12), # bedroom -> lamp_bedroom_switch
                (2, 13), # bathroom -> lamp_bathroom_switch
                (3, 14), # living room -> lamp_living_room_switch
                (4, 15)  # kitchen -> lamp_kitchen_switch
            ]
            cursor.executemany('INSERT INTO room_devices (room_id, device_id) VALUES (?, ?)', room_devices)
            
            self.connection.commit()
            print("Data inserted successfully")
        except Error as e:
            print(f"Error inserting data: {e}")
    def get_device_state(self, device_type):
        """Get the state of a device by its type."""
        cursor = self.connection.cursor()
        cursor.execute('SELECT state FROM devices WHERE type = ?', (device_type,))
        result = cursor.fetchone()
        return result[0] if result else None

    def update_device_state(self, device_type, new_state):
        """Update the state of a device by its type."""
        cursor = self.connection.cursor()
        cursor.execute('UPDATE devices SET state = ? WHERE type = ?', (new_state, device_type))
        self.connection.commit()



    def close_connection(self):
        if self.connection:
            self.connection.close()
            print("Connection closed")

 
DB_FILE = os.path.join(os.path.dirname(__file__), 'data.db')

