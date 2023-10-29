"""Functions handling the configuration and connection to the postgres server
"""

import os
from shutil import which
import configparser

# === GLOBALS ===
from spacer.globals import _connection_config_path, _spacer_config_dir

# === FUNCTIONS ===


def check_configuration_file() -> bool:
    """Checking if the configuration file exists
    """

    # Create the .spacer dir if not existing
    if os.path.isdir(_spacer_config_dir) == False:
        os.makedirs(_spacer_config_dir)

    if os.path.isfile(_connection_config_path):
        return True
    else:
        return False


def create_config_file(config_params: dict) -> int:
    """
    """
    if check_configuration_file() == False:
        config = configparser.ConfigParser()

        config.read(_connection_config_path)
        config.add_section('connection')
        config.set('connection', 'dbname', config_params['dbname'])
        config.set('connection', 'user', config_params['user'])
        config.set('connection', 'password', config_params['password'])
        config.set('connection', 'host', config_params['host'])
        config.set('connection', 'port', str(config_params['port']))

        with open(_connection_config_path, 'w') as f:
            config.write(f)

    return 0


def get_config_dict_from_file() -> dict:
    """Simple wrapper to get the params from the config file
    """
    if check_configuration_file() == False:
        raise FileNotFoundError("No config file found at: {0:s}".format(
            _connection_config_path))

    else:
        config = configparser.ConfigParser(allow_no_value=True)
        config.read(_connection_config_path)

        config_params_dict = dict(config['connection'])

        return config_params_dict


def check_password() -> bool:
    """
    """
    config_dict = get_config_dict_from_file()

    # Check if the password exist

    if config_dict['password'] != str(None):
        return True
    else:
        return False


def get_upasswd() -> str:
    """
    """
    config_dict = get_config_dict_from_file()
    return config_dict['password']


def set_upasswd(upasswd) -> int:
    """
    """
    config = configparser.ConfigParser()
    config.read(_connection_config_path)

    config.set('connection', 'password', upasswd)

    with open(_connection_config_path, "w+") as configfile:
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
