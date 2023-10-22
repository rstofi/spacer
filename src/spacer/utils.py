"""Utility functions for spacer
"""

import os
from shutil import which
from configparser import ConfigParser

# ===Import globals
from spacer.globals import _config_path

# === FUNCTIONS ===
def get_logo() -> str:
    """
    """

    logo_string = r"                                " + '\n' + \
r"  ___ _ __   __ _  ___ ___ _ __ " + '\n' + \
r" / __| '_ \ / _` |/ __/ _ \ '__|" + '\n' + \
r" \__ \ |_) | (_| | (_|  __/ |   " + '\n' + \
r" |___/ .__/ \__,_|\___\___|_|   " + '\n' + \
r"     | |                        " + '\n' + \
r"     |_|                        " + '\n\n'

    return logo_string

def check_configuration_file() -> str:
    """Checking if the configuration file exists
    """

    if os.path.isfile(_config_path):
        return True
    else:
        return False

def create_config_file(config_params) -> int:
    """
    """

    if not check_configuration_file():
        config = ConfigParser()

        config.read(_config_path)
        config.add_section('main')
        config.set('main', 'dbname', config_params['dbname'])
        config.set('main', 'user', config_params['user'])
        config.set('main', 'host', config_params['host'])

        if config_params['port'] != None:
            config.set('main', 'port', config_params['port'])

        with open(_config_path, 'w') as f:
            config.write(f)
    
    else:
        raiseError('Config file already exist!')

    return 0

def check_database_connection() -> bool:
    """Checking if the database is installed, and can be accessed.
    """

    return False

# === MAIN ===
if __name__ == "__main__":
    pass
