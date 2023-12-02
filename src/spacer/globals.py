"""Global variables
"""

import os

# === Paths
# Get the absolute path to the project's root directory
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))

# === DB settings
DEAFAULT_DB_NAME = 'spacer.db'
DEAFAULT_DB_PATH = os.path.join(PROJECT_ROOT,'data/{0:s}'.fomrat(DEAFAULT_DB_NAME))

# === TUI settings
SPACER_LOGO = r"                                " + '\n' + \
    r"  ___ _ __   __ _  ___ ___ _ __ " + '\n' + \
    r" / __| '_ \ / _` |/ __/ _ \ '__|" + '\n' + \
    r" \__ \ |_) | (_| | (_|  __/ |   " + '\n' + \
    r" |___/ .__/ \__,_|\___\___|_|   " + '\n' + \
    r"     | |                        " + '\n' + \
    r"     |_|                        " + '\n\n'

CONSLOLE_PROMPT_TEXT = 'spacer:> '

EXIT_MESSAGE = '\nSee you cowgirl,\nsomeday, somewhere.'

# === Default key binding dictionary
DEFAULT_KEY_BINDINGS = {
    'q': 'Quit spacer',
    'h': 'Show help',
    'r': 'Run sql script'
}

# === MAIN ===
if __name__ == "__main__":
    pass
