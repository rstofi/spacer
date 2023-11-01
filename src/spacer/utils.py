"""Utility functions
"""

import os
import configparser

from spacer.globals import  _spacer_config_dir, _spacer_config_path

# === FUNCTIONS ===

def check_configuration_file() -> bool:
    """Checking if the configuration file exists
    """

    # Create the .spacer dir if not existing
    if os.path.isdir(_spacer_config_dir) == False:
        os.makedirs(_spacer_config_dir)

    if os.path.isfile(_spacer_config_path):
        return True
    else:
        return False


def create_config_file(config_params:dict) -> int:
    """
    """
    if check_configuration_file() == False:
        config = configparser.ConfigParser()

        config.read(_spacer_config_path)
        config.add_section('spacer')
        config.set('spacer', 'connection_config_path',
                config_params['connection_config_path'])

        with open(_spacer_config_path, 'w') as f:
            config.write(f)

    return 0

def get_config_dict_from_file() -> dict:
    """Simple wrapper to get the params from the config file
    """
    if check_configuration_file() == False:
        raise FileNotFoundError("No config file found at: {0:s}".format(
            _spacer_config_path))

    else:
        config = configparser.ConfigParser(allow_no_value=True)
        config.read(_spacer_config_path)

        config_params_dict = dict(config['spacer'])

        return config_params_dict

# === MAIN ===
if __name__ == "__main__":
    pass
