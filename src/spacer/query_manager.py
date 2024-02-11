"""Module responsible for querying the database
"""

import sys
import os
import pandas as pd
import markdown
from spacer.formatting import md_par
from spacer.globals import PROJECT_ROOT

# Append the project root to sys.path
sys.path.append(PROJECT_ROOT)

# === Classes


class QueryManager:
    """
    """
    # === METHODS ===

    def __init__(self, sqlite3_cursor, get_db_connection_function):
        self.cursor = sqlite3_cursor  # squlite.Cursor object
        self.get_db_connection = get_db_connection_function  # This is a function
        self.spacer_sql_files_path = os.path.join(PROJECT_ROOT, 'sql/')
        self.query = None  # actual query string

    def find_spacer_sql_file(self, file_name: str) -> str:
        """
        File name does not need the .sql extension
        """
        return os.path.join(self.spacer_sql_files_path, file_name + '.sql')

    # === Formatting options
    def query_result_to_pandas_df(self) -> pd.DataFrame:
        """
        Convert the query result to pandas DataFrame
        """

        query_results_df = pd.DataFrame(self.cursor.fetchall())

        query_results_df.columns = [description[0]
                                    for description in self.cursor.description]

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

    # === General query helpers
    def execute_sql_file(self, script_path) -> None:
        """
        Executes an SQL script to create tables.

        NOTE: this method executes **every** query in the file

        NOTE this is a query that should be moved into

        Args:
            script_path (str): Path to the SQL script file.
        """
        with open(script_path, 'r') as sql_file:
            sql_script = sql_file.read()

        self.cursor.executescript(sql_script)

    # === Companies queries
    def check_if_company_exists(self, company_name: str) -> bool:
        """
        """
        self.query = extract_query(self.find_spacer_sql_file('companies'),
                                   'check_if_company_exists')

        self.cursor.execute(self.query, (company_name,))

        # self.cursor.fetchone() None or tuple of the company names

        if self.cursor.fetchone() is None:
            return False
        else:
            return True

    def fetch_company_row(self, company_name: str) -> str:
        """
        """
        if self.check_if_company_exists(company_name):
            self.query = extract_query(self.find_spacer_sql_file('companies'),
                                       'fetch_company_row')

            self.cursor.execute(self.query, [company_name])

            return self.query_result_to_md()

        else:
            raise ValueError(
                "Company '{0:s}' not found in database!".format(company_name))

    def fetch_company_id(self, company_name: str) -> int:
        """
        """
        if self.check_if_company_exists(company_name):
            self.query = extract_query(self.find_spacer_sql_file('companies'),
                                       'fetch_company_id')

            self.cursor.execute(self.query,
                                [company_name])
        else:
            raise ValueError(
                "Company '{0:s}' not found in database!".format(company_name))

        company_row = self.query_result_to_pandas_df()

        # .iloc[n] select the nth value from the column
        return int(company_row['id'].iloc[0])

    def add_company(self, company_row_dict: dict) -> None:
        """
        """

        if self.check_if_company_exists(company_row_dict['name']) == False:
            # Insert data into companies table
            self.query = extract_query(self.find_spacer_sql_file('companies'),
                                       'add_company')

            self.cursor.execute(self.query,
                                (company_row_dict['name'],
                                 company_row_dict['is_recruitment_agency'],
                                 company_row_dict['website'],
                                 company_row_dict['comments']))

            # Commit changes to DB
            db_connection = self.get_db_connection()
            db_connection.commit()


# === Functions
def extract_query(sql_script: str, query_name: str) -> str:
    """Only queries starting with the comment

    -- Spacer: {query_name}

    are converted to strings, but ONLY if the next query is also has the

    -- Spacer: {query_name}

    comment. Or else, everything is converted from below the comment into a string
    """
    query_start = f"-- spacer: {query_name}"
    query_end = "-- spacer"

    with open(sql_script, 'r') as sql_file:
        lines = sql_file.readlines()

    start_index = None
    end_index = None
    for i, line in enumerate(lines):
        if query_start in line:
            start_index = i + 1  # Start from the next line after identifier
        elif query_end in line and start_index is not None:
            end_index = i
            break  # Stop at the beginning of the next query

    if start_index is not None:
        if end_index is None:  # If it's the last query in the file
            end_index = len(lines)
        query_lines = lines[start_index:end_index]
        return ''.join(query_lines).strip()
    else:
        raise ValueError(
            f"Query named '{query_name}' not found in {sql_file}.")


# === Functions

# === MAIN ===
if __name__ == '__main__':
    main()
