"""Global variables
"""

import os

# === The logo
SPACER_LOGO = r"                                " + '\n' + \
    r"  ___ _ __   __ _  ___ ___ _ __ " + '\n' + \
    r" / __| '_ \ / _` |/ __/ _ \ '__|" + '\n' + \
    r" \__ \ |_) | (_| | (_|  __/ |   " + '\n' + \
    r" |___/ .__/ \__,_|\___\___|_|   " + '\n' + \
    r"     | |                        " + '\n' + \
    r"     |_|                        " + '\n\n'

# === Default key binding dictionary
DEFAULT_KEY_BINDINGS = {
    'q': 'Quit spacer',
    'h': 'Show help',
    'd': 'Show database connection configuration'
}

# === Console prompt text
CONSLOLE_PROMPT_TEXT = 'spacer:> '

# === Absolute path to the configuration folder, conncetion config and password files
SPACER_CONFIG_DIR = os.path.join(os.path.expanduser('~'), '.spacer')
SPACER_CONFIG_PATH = os.path.join(SPACER_CONFIG_DIR, 'config.ini')


# === Default connection_configuration file parameters
CONNECTION_CONFIG_PATH = os.path.join(SPACER_CONFIG_DIR, 'db_conncetion.ini')
CONNECTION_CONFIG_DEFAULT_PARAMS = {'dbname': 'spacer_job_board',
                                    'user': 'postgres',
                                    'password': None,
                                    'host': 'localhost',
                                    'port': None}

# === MAIN ===
if __name__ == "__main__":
    pass
