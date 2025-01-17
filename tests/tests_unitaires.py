import pytest
import sqlite3
import os
from database import __database__ as db

@pytest.fixture
def setup_database():
    # Setup: Create a test database and insert initial data
    db_file = "/home/alexis_lantier/mini-projet-projet-chalet/tests/test_data.db"
    database = db.Database(db_file)
    database.create_tables()
    database.insert_data()
    yield database
    # Teardown: Close the database connection and delete the test database file
    database.close_connection()
    if os.path.exists(db_file):
        os.remove(db_file)

def test_update_all_to_one(setup_database):
    database = setup_database

    # Update all device states to '1'
    cursor = database.connection.cursor()
    cursor.execute('UPDATE devices SET state = ?', ('1',))
    database.connection.commit()

    # Verify that all device states are '1'
    cursor.execute('SELECT state FROM devices')
    results = cursor.fetchall()
    for result in results:
        assert result[0] == '1', f"Expected state '1', but got {result[0]}"

if __name__ == "__main__":
    pytest.main()