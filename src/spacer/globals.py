"""Global variables
"""

import os

# === The logo
_spacer_logo = r"                                " + '\n' + \
    r"  ___ _ __   __ _  ___ ___ _ __ " + '\n' + \
    r" / __| '_ \ / _` |/ __/ _ \ '__|" + '\n' + \
    r" \__ \ |_) | (_| | (_|  __/ |   " + '\n' + \
    r" |___/ .__/ \__,_|\___\___|_|   " + '\n' + \
    r"     | |                        " + '\n' + \
    r"     |_|                        " + '\n\n'

# === Default key binding dictionary
_default_key_bindings = {'h': 'Show help',
                         'q': 'Quit spacer'}

# === Console prompt text
_console_prompt_text = 'spacer:> '

# === Absolute path to the configuration folder, conncetion config and password files
_spacer_config_dir = os.path.join(os.path.expanduser('~'), '.spacer')
_spacer_config_path = os.path.join(_spacer_config_dir, 'config.ini')
_connection_config_path = os.path.join(_spacer_config_dir, 'db_conncetion.ini')

# === Default connection_configuration file parameters
_connection_config_default_params = {'dbname': 'spacer_job_board',
                                     'user': 'postgres',
                                     'password': None,
                                     'host': 'localhost',
                                     'port': None}

# === MAIN ===
if __name__ == "__main__":
    pass
