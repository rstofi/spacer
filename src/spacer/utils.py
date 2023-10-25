"""Utility functions for spacer
"""

import os
from shutil import which
import configparser

# === GLOBALS ===
from spacer.globals import _config_path

# === FUNCTIONS ===
def check_configuration_file() -> str:
    """Checking if the configuration file exists
    """

    if os.path.isfile(_config_path):
        return True
    else:
        return False

def create_config_file(config_params:dict) -> int:
    """
    """

    if not check_configuration_file():
        config = configparser.ConfigParser()

        config.read(_config_path)
        config.add_section('connection')
        config.set('connection', 'dbname', config_params['dbname'])
        config.set('connection', 'user', config_params['user'])
        config.set('connection', 'host', config_params['host'])
        config.set('connection', 'port', str(config_params['port']))

        with open(_config_path, 'w') as f:
            config.write(f)
    
    else:
        raiseError('Config file already exist!')

    return 0

def get_config_dict_from_file() -> dict:
    """Simple wrapper to get the params from the config file
    """
    if check_configuration_file() == False:
        raise FileNotFoundError("No config file found at: {0:s}".format(_config_path))

    else:
        config = configparser.ConfigParser(allow_no_value=True)
        config.read(_config_path)

        config_params_dict = dict(config['connection'])

        return config_params_dict

def check_database_connection() -> bool:
    """Checking if the database is installed, and can be accessed.
    """

    return False

# === MAIN ===
if __name__ == "__main__":
    pass
