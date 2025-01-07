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

# Create a table
def create_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS home_automation (
                id INTEGER PRIMARY KEY,
                room TEXT NOT NULL,
                type TEXT NOT NULL,
                state TEXT NOT NULL
            )
        ''')
        print("Table created successfully")
    except Error as e:
        print(f"Error creating the table: {e}")

# Insert data into the table
def insert_data(connection, data):
    """Insert data into the home_automation table."""
    try:
        cursor = connection.cursor()
        cursor.executemany('''
            INSERT INTO home_automation (room, type, state) VALUES (?, ?, ?)
        ''', data)
        connection.commit()
        print("Data inserted successfully")
    except Error as e:
        print(f"Error inserting data: {e}")

# Example usage

db_file = "database/data.db"
connection = create_connection(db_file)

if connection is not None:
    create_table(connection)
    
    # Data to insert
    data = [
        ('bathroom', 'lamp', 'off'),
        ('kitchen', 'outlet', 'on'),
        ('bedroom', 'skylight', 'closed'),
        ('living room', 'heater', 'on'),
        ('living room', 'temperature sensor', '22°C'),
        ('living room', 'humidity sensor', '45%')
    ]
    
    insert_data(connection, data)
    
    # Close the connection
    connection.close()