"""Script that initializes an empty default database using the `spacer` schema 

The database will be created as: data/spacer.db (see the default values)
"""

import os

# Get the absolute path to the project's root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Append the project root to sys.path
sys.path.append(project_root)


# === Classes
class DatabaseCreator:
    """
    """
    def __init__(self, database_path):
        





# === Functions
def main() -> None:
    """
    Main function to execute the DatabaseCreator class.
    """
    db_creator = DatabaseCreator()

    db_populator.insert_csv_to_db()

# === MAIN ===
if __name__ == '__main__':
    main()