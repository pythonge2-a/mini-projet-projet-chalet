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
            ('lamp_bedroom', 'off'),
            ('lamp_bathroom', 'off'),
            ('lamp_living_room', 'off'),
            ('lamp_kitchen', 'off'),
            ('heater_hedroom', 'off'),
            ('heater_rest_of_chalet', 'off'),
            ('skylight', 'closed'),
            ('luminosity_living_room', 'normal'),
            ('temperature sensor_bedroom', '18°C'),
            ('temperature sensor_rest_of_chalet', '20°C'),
            ('humidity sensor_all', '45%')
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

# Example usage

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