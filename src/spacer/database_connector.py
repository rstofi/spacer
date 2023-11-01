"""Functions handling the configuration and connection to the postgres server
"""

import os
from shutil import which
import configparser

# === GLOBALS ===
from spacer.globals import _connection_config_path, _spacer_config_dir

# === FUNCTIONS ===
def check_connection_configuration_file(conn_config_path:str=_connection_config_path) -> bool:
    """Checking if the configuration file exists
    """
    if os.path.isfile(conn_config_path):
        return True
    else:
        return False


def create_connection_config_file(config_params: dict,
                        conn_config_path:str=_connection_config_path) -> int:
    """
    """
    if check_connection_configuration_file(conn_config_path) == False:
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


def get_connection_config_dict_from_file(conn_config_path:str=_connection_config_path) -> dict:
    """Simple wrapper to get the params from the config file
    """
    if check_connection_configuration_file(conn_config_path) == False:
        raise FileNotFoundError("No config file found at: {0:s}".format(
            conn_config_path))

    else:
        config = configparser.ConfigParser(allow_no_value=True)
        config.read(conn_config_path)

        config_params_dict = dict(config['connection'])

        return config_params_dict


def check_password(conn_config_path:str=_connection_config_path) -> bool:
    """
    """
    config_dict = get_connection_config_dict_from_file(conn_config_path)

    # Check if the password exist

    if config_dict['password'] != str(None):
        return True
    else:
        return False


def get_upasswd(conn_config_path:str=_connection_config_path) -> str:
    """
    """
    config_dict = get_connection_config_dict_from_file(conn_config_path)
    return config_dict['password']


def set_upasswd(upasswd, conn_config_path:str=_connection_config_path) -> int:
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
