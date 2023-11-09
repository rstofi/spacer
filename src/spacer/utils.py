"""Utility functions
"""

import os
import configparser

from spacer.globals import  SPACER_CONFIG_DIR, SPACER_CONFIG_PATH, \
                        CONNECTION_CONFIG_PATH

# === FUNCTIONS ===

def check_spacer_configuration_file() -> bool:
    """Checking if the configuration file exists
    """

    # Create the .spacer dir if not existing
    if os.path.isdir(SPACER_CONFIG_DIR) == False:
        os.makedirs(SPACER_CONFIG_DIR)

    return os.path.isfile(SPACER_CONFIG_PATH)


def create_config_file(config_params:dict) -> int:
    """
    """
    if check_spacer_configuration_file() == False:
        config = configparser.ConfigParser()

        config.read(SPACER_CONFIG_PATH)
        config.add_section('spacer')
        config.set('spacer', 'connection_config_path',
                config_params['connection_config_path'])
        config.set('spacer', 'verbose',
                config_params['verbose'])

        with open(SPACER_CONFIG_PATH, 'w') as f:
            config.write(f)

    return 0

def get_config_dict_from_file() -> dict:
    """Simple wrapper to get the params from the config file
    """
    if check_spacer_configuration_file() == False:
        raise FileNotFoundError("No config file found at: {0:s}".format(
            SPACER_CONFIG_PATH))

    else:
        config = configparser.ConfigParser(allow_no_value=True)
        config.read(SPACER_CONFIG_PATH)

        config_params_dict = dict(config['spacer'])

        return config_params_dict

def create_connection_config_file(config_params: dict,
                        conn_config_path:str=CONNECTION_CONFIG_PATH) -> int:
    """
    """
    if not os.path.isfile(conn_config_path):
        config = configparser.ConfigParser()

        config.read(conn_config_path)
        config.add_section('connection')
        config.set('connection', 'dbname', config_params['dbname'])
        config.set('connection', 'user', config_params['user'])
        config.set('connection', 'password', config_params['password'])
        config.set('connection', 'host', config_params['host'])
        config.set('connection', 'port', str(config_params['port']))

        with open(conn_config_path, 'w') as f:
            config.write(f)

    return 0


def get_connection_config_dict_from_file(conn_config_path:str=CONNECTION_CONFIG_PATH) -> dict:
    """Simple wrapper to get the params from the config file
    """
    if not os.path.isfile(conn_config_path):
        raise FileNotFoundError("No config file found at: {0:s}".format(
            conn_config_path))

    else:
        config = configparser.ConfigParser(allow_no_value=True)
        config.read(conn_config_path)

        config_params_dict = dict(config['connection'])

        return config_params_dict


def check_password_exists_in_config(conn_config_path:str=CONNECTION_CONFIG_PATH) -> bool:
    """
    """
    config_dict = get_connection_config_dict_from_file(conn_config_path)

    # Check if the password exist
    return config_dict['password'] != str(None)


def get_upasswd(conn_config_path:str=CONNECTION_CONFIG_PATH) -> str:
    """
    """
    config_dict = get_connection_config_dict_from_file(conn_config_path)
    return config_dict['password']


def set_upasswd(upasswd, conn_config_path:str=CONNECTION_CONFIG_PATH) -> int:
    """
    """
    config = configparser.ConfigParser()
    config.read(conn_config_path)

    config.set('connection', 'password', upasswd)

    with open(conn_config_path, "w+") as configfile:
        config.write(configfile)

    return 0


def connection_config_display_skip(config_params: dict) -> list:
    """Returns a list of parameters to NOT show in the TUI about the connection
    """

    display_skip_list = []

    for key, val in config_params.items():
        if val == str(None):
            display_skip_list.append(key)
        elif key == 'password':
            display_skip_list.append(key)

    return display_skip_list



# === MAIN ===
if __name__ == "__main__":
    pass
