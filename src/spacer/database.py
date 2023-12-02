"""Classes handling the database creation and querying
"""

import os
import sys
import sqlite3
from spacer.globals import PROJECT_ROOT, DEAFAULT_DB_PATH

# Append the project root to sys.path
sys.path.append(PROJECT_ROOT)

# === Classes
class DatabaseHandler:
    """
    """
    def __init__(self, db_path):
        """
        """
        self.db_path = db_path
        self.db_connection = None # sqlite3.Connection object
        self.cursor = None # squlite.Cursor object


    def create_memory_db_connection(self) -> None:
        """
        Creates an in-memory SQLite database connection.
        """
        try:
            self.db_connection = sqlite3.connect(':memory:')
        except Exception as e:
            print(e)

        # Generate a cursor
        self.cursor = self.db_connection.cursor()

    def close_db_connection(self) -> None:
        """
        Closes the SQLite database connection.
        """
        self.cursor.close()
        self.db_connection.close()

    def execute_sql_file(self,script_path) -> None:
        """
        Executes an SQL script to create tables.

        NOTE: this method executes **every** query in the file

        Args:
            script_path (str): Path to the SQL script file.
        """
        with open(script_path, 'r') as sql_file:
            sql_script = sql_file.read()

        self.cursor.executescript(sql_script)


# === Functions
def create_empty_db(db_path, schema_path) -> None:
    """Create an empty database if not existing
    """
    if os.path.isfile(db_path):
        return ValueError('Database already exist: {0:s}'.fomrat(db_path))

    # Create empty database and parent directories if needed
    if not os.path.exists(os.path.abspath(os.path.dirname(db_path))):
        os.makedirs(os.path.abspath(os.path.dirname(db_path)))


    # Create database
    db_handler = DatabaseHandler(db_path)

    db_handler.create_memory_db_connection()

    # Create database schema
    db_handler.execute_sql_file(schema_path)

    db_disk = sqlite3.connect(db_handler.db_path)
    db_handler.db_connection.backup(db_disk)

    # Close connections
    db_handler.close_db_connection()
    db_disk.close()

# === MAIN ===
if __name__ == '__main__':
    main()