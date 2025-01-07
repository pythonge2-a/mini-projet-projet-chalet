import sqlite3
from sqlite3 import Error

# Create a connection to the database
def create_connection(db_file):
    """Create a connection to the SQLite database specified by db_file."""
    connection = None
    try:
        connection = sqlite3.connect(db_file)
        print(f"Successfully connected to the database {db_file}")
    except Error as e:
        print(f"Error connecting to the database: {e}")
    return connection

# Create tables
def create_tables(connection):
    try:
        cursor = connection.cursor()
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
        print("Tables created successfully")
    except Error as e:
        print(f"Error creating the tables: {e}")

# Insert data into the tables
def insert_data(connection):
    try:
        cursor = connection.cursor()
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
            ('luminosity_living_room[lux]', 200),
            ('temperature_bedroom[°C]', 18),
            ('temperature_rest_of_chalet[°C]', 20),
            ('humidity_all[%]', 45)
        ]
        cursor.executemany('INSERT INTO devices (type, state) VALUES (?, ?)', devices)
        
        # Insert room_devices relationships
        room_devices = [
            (1, 1),  
            (2, 2),  
            (3, 3),  
            (4, 4),  
            (1, 5),  
            (2, 6),  
            (3, 6),  
            (4, 6),  
            (3, 7),  
            (3, 8),  
            (1, 9),  
            (2, 10), 
            (3, 10),  
            (4, 10),  
            (1, 11),  
            (2, 11),  
            (3, 11),  
            (4, 11)   
        ]
        cursor.executemany('INSERT INTO room_devices (room_id, device_id) VALUES (?, ?)', room_devices)
        
        connection.commit()
        print("Data inserted successfully")
    except Error as e:
        print(f"Error inserting data: {e}")

def get_device_state(connection, device_type):
    """Get the state of a device by its type."""
    cursor = connection.cursor()
    cursor.execute('SELECT state FROM devices WHERE type = ?', (device_type,))
    result = cursor.fetchone()
    return result[0] if result else None

def update_device_state(connection, device_type, new_state):
    """Update the state of a device by its type."""
    cursor = connection.cursor()
    cursor.execute('UPDATE devices SET state = ? WHERE type = ?', (new_state, device_type))
    connection.commit()


#usage
db_file = "database/data.db"
connection = create_connection(db_file)

if connection is not None:
    create_tables(connection)
    insert_data(connection)
    # Close the connection
    connection.close()
    print("Connection closed")
else:
    print("Failed to create the database connection")

