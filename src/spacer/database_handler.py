"""Classes handling the database creation and querying
"""

import os
import sys
import sqlite3
import pandas as pd
import markdown
from spacer.globals import PROJECT_ROOT, DEAFAULT_DB_PATH
from spacer.formatting import md_par

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
        self.db_connection = None # sqlite3.Connection object
        self.cursor = None # squlite.Cursor object

    # === General DB handling
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

    def create_db_connection(self) -> None:
        """
        """
        try:
            self.db_connection = sqlite3.connect(self.db_path)
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

    def query_result_to_pandas_df(self) -> pd.DataFrame:
        """
        Convert the query result to pandas DataFrame
        """

        query_results_df = pd.DataFrame(self.cursor.fetchall())

        query_results_df.columns = [description[0] for description in self.cursor.description]

        return query_results_df

    def query_result_to_md(self) -> str:
        """
        Convert the query result to pandas DataFrame
        Then convert this to markdown format (str)
        """

        query_results_df = self.query_result_to_pandas_df()

        # Create formatted output string
        query_result_string = md_par()
        query_result_string += query_results_df.to_markdown(index=False)
        query_result_string += md_par()

        return query_result_string

    # === Check database methods
    def check_if_company_exists(self, company_name:str) -> bool:
        """
        """
        self.cursor.execute('SELECT name FROM companies WHERE name = ?',
                            (company_name,))

        # self.cursor.fetchone() None or tuple of the company names
            
        if self.cursor.fetchone() == None:
            return False
        else:
            return True

    def fetch_company_row(self, company_name:str) -> str:
        """
        """
        if self.check_if_company_exists(company_name):
            self.cursor.execute('''
                SELECT *
                FROM companies
                WHERE name = ?
                ''',
                [company_name])

            return self.query_result_to_md()

        else:
            raise ValueError("Company '{0:s}' not found in database!".format(company_name))

    def fetch_company_id(self, company_name:str) -> int:
        """
        """
        if self.check_if_company_exists(company_name):
            self.cursor.execute('''
                SELECT id
                FROM companies
                WHERE name = ?
                ''',
                [company_name])
        else:
            raise ValueError("Company '{0:s}' not found in database!".format(company_name))

        company_row = self.query_result_to_pandas_df() 

        # .iloc[n] select the nth value from the column
        return int(company_row['id'].iloc[0])

    # === Insert to database methods
    def add_company(self, company_row_dict:dict) -> None:
        """
        """

        if self.check_if_company_exists(company_row_dict['name']) == False:
            # Insert data into companies table
            self.cursor.execute('''
                INSERT INTO companies(name, is_recruitment_agency, website, comments)
                VALUES (?, ?, ?, ?)
                ''',
                (company_row_dict['name'], 
                company_row_dict['is_recruitment_agency'],
                company_row_dict['website'],
                company_row_dict['comments']))

            # Commit changes to DB
            self.db_connection.commit()

# === Functions
def create_empty_db(db_path, schema_path) -> None:
    """Create an empty database if not existing
    """
    if os.path.isfile(db_path):
        return ValueError('Database already exist: {0:s}'.format(db_path))

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