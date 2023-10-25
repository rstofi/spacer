"""Global variables
"""

import os

# === The logo
global _spacer_logo
_spacer_logo = r"                                " + '\n' + \
r"  ___ _ __   __ _  ___ ___ _ __ " + '\n' + \
r" / __| '_ \ / _` |/ __/ _ \ '__|" + '\n' + \
r" \__ \ |_) | (_| | (_|  __/ |   " + '\n' + \
r" |___/ .__/ \__,_|\___\___|_|   " + '\n' + \
r"     | |                        " + '\n' + \
r"     |_|                        " + '\n\n'

# === Default key binding dictionary
global _default_key_bindings
_default_key_bindings = {'h':'Show help',
                        'q':'Quit spacer'}

# === Absolute path to the configuration path
global _config_path
_config_path = os.path.join(os.path.expanduser('~'),'.spacer.ini')

# === Default configuration file parameters
global _config_default_params

_config_default_params = {'dbname' : 'spacer_job_board',
                'user' : 'postgres',
                'host' : 'localhost',
                'port' : None}