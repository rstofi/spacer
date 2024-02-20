"""Module responsible for database connection and setup
"""

import os
import sys
import sqlite3
from spacer.globals import PROJECT_ROOT, DEAFAULT_DB_PATH
from spacer.query_manager import QueryManager

# Append the project root to sys.path
sys.path.append(PROJECT_ROOT)

# === Classes


class DatabaseHandler:
    """
    """
    # === METHODS ===

    def __init__(self, db_path):
        """
        """
        self.db_path = db_path
        self.db_connection = None  # sqlite3.Connection object
        self.cursor = None  # squlite.Cursor object
        self.qery_manager = None  # QueryManager

    # === General DB handling
    def get_database_connection_for_querying(self) -> sqlite3.Connection:
        """
        """
        return self.db_connection

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
        self.query_manager = QueryManager(
            self.cursor, self.get_database_connection_for_querying)

    def create_db_connection(self) -> None:
        """
        """
        try:
            self.db_connection = sqlite3.connect(self.db_path)
        except Exception as e:
            print(e)

        # Generate a cursor
        self.cursor = self.db_connection.cursor()
        self.query_manager = QueryManager(
            self.cursor, self.get_database_connection_for_querying)

    def close_db_connection(self) -> None:
        """
        Closes the SQLite database connection.
        """
        self.query_manager = None
        del self.query_manager
        self.cursor.close()
        self.db_connection.close()

# === Functions


def create_empty_db(db_path, schema_path) -> None:
    """Create an empty database if not existing
    """
    if os.path.isfile(db_path):
        return ValueError(f'Database already exist: {db_path}')

    # Create empty database and parent directories if needed
    if not os.path.exists(os.path.abspath(os.path.dirname(db_path))):
        os.makedirs(os.path.abspath(os.path.dirname(db_path)))

    # Create database
    db_handler = DatabaseHandler(db_path)

    db_handler.create_memory_db_connection()

    # Create database schema
    db_handler.query_manager.execute_sql_file(schema_path)

    db_disk = sqlite3.connect(db_handler.db_path)
    db_handler.db_connection.backup(db_disk)

    # Close connections
    db_handler.close_db_connection()
    db_disk.close()


# === MAIN ===
if __name__ == '__main__':
    main()
